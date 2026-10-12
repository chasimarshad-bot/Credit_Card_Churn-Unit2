"""Snapshot classification with train-only fitting and validation-only decisions."""
import json
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score,
    confusion_matrix, fbeta_score, precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from .data import FEATURES, OUTPUT

SEED = 42


def split_data(df):
    """60/20/20 stratified split; retain row indices to audit disjointness."""
    train, remainder = train_test_split(df, test_size=0.4, stratify=df.Churn, random_state=SEED)
    validation, test = train_test_split(remainder, test_size=0.5,
                                      stratify=remainder.Churn, random_state=SEED)
    return train, validation, test


def candidates(features=FEATURES):
    # Imputation/scaling remain inside CV; no learned transformation sees validation/test.
    return {
        'Logistic regression': make_pipeline(SimpleImputer(strategy='median'), StandardScaler(),
            LogisticRegression(class_weight='balanced', max_iter=2000, random_state=SEED)),
        'Random forest': make_pipeline(SimpleImputer(strategy='median'),
            RandomForestClassifier(n_estimators=150, max_depth=10, min_samples_leaf=5,
                                   class_weight='balanced_subsample', random_state=SEED, n_jobs=1))}


def metrics(y, scores, threshold):
    predicted = (scores >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0,1]).ravel()
    return {'threshold': float(threshold), 'accuracy': accuracy_score(y, predicted),
            'balanced_accuracy': balanced_accuracy_score(y, predicted),
            'precision': precision_score(y, predicted, zero_division=0),
            'recall': recall_score(y, predicted, zero_division=0),
            'f2': fbeta_score(y, predicted, beta=2, zero_division=0),
            'average_precision': average_precision_score(y, scores),
            'roc_auc': roc_auc_score(y, scores),
            'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp)}


def threshold_search(y, scores):
    table = pd.DataFrame([metrics(y, scores, t) for t in np.arange(0.05,0.951,0.025)])
    feasible = table[table.precision.ge(0.60)]
    # The 60% floor is an illustrative stakeholder constraint, not an observed business cost.
    pool = feasible if not feasible.empty else table
    chosen = pool.sort_values(['recall','precision','threshold'], ascending=[False,False,False]).iloc[0]
    return float(chosen.threshold), table, not feasible.empty


def run_modelling(df, save=True):
    train, validation, test = split_data(df)
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED)
    rows = []
    models = candidates()
    for name, model in models.items():
        scores = cross_validate(model, train[FEATURES], train.Churn, cv=cv,
            scoring={'ap':'average_precision','roc':'roc_auc'}, n_jobs=1)
        rows.append({'model':name, 'cv_ap_mean': scores['test_ap'].mean(),
                     'cv_ap_sd':scores['test_ap'].std(ddof=1),
                     'cv_roc_mean':scores['test_roc'].mean()})
    comparison = pd.DataFrame(rows).sort_values('cv_ap_mean', ascending=False)
    name = comparison.iloc[0]['model']
    model = clone(models[name]).fit(train[FEATURES], train.Churn)
    val_scores = model.predict_proba(validation[FEATURES])[:,1]
    threshold, threshold_table, feasible = threshold_search(validation.Churn, val_scores)
    # Only after model and threshold are locked is the test split scored.
    test_scores = model.predict_proba(test[FEATURES])[:,1]
    final = metrics(test.Churn, test_scores, threshold)
    dummy = DummyClassifier(strategy='prior').fit(train[FEATURES], train.Churn)
    baseline = metrics(test.Churn, dummy.predict_proba(test[FEATURES])[:,1], 0.5)
    important = permutation_importance(model, validation[FEATURES], validation.Churn,
        scoring='average_precision', n_repeats=5, random_state=SEED, n_jobs=1)
    importance = pd.DataFrame({'feature': FEATURES, 'ap_decrease':important.importances_mean,
                              'sd':important.importances_std}).sort_values('ap_decrease',ascending=False)
    # Sensitivity removes a feature whose timing may overlap account closure.
    safe_features = [f for f in FEATURES if f != 'Contacts_Count_12_mon']
    sensitivity_model = clone(models[name]).fit(train[safe_features], train.Churn)
    sensitivity_ap = average_precision_score(validation.Churn,
                       sensitivity_model.predict_proba(validation[safe_features])[:,1])
    rng = np.random.default_rng(SEED)
    boot = []
    y = test.Churn.to_numpy()
    for _ in range(300):
        positions = rng.integers(0, len(y), len(y))
        if len(np.unique(y[positions])) == 2:
            boot.append(average_precision_score(y[positions],test_scores[positions]))
    result = {'selected_model':name, 'seed':SEED, 'features':FEATURES,
              'split_sizes':{'train':len(train),'validation':len(validation),'test':len(test)},
              'split_churn_rates':{k:float(v.Churn.mean()) for k,v in
                                   [('train',train),('validation',validation),('test',test)]},
              'validation_precision_floor_met':feasible,
              'validation_selected':metrics(validation.Churn,val_scores,threshold),
              'test':final, 'dummy_test':baseline,
              'test_ap_bootstrap_95':np.quantile(boot,[0.025,0.975]).tolist(),
              'validation_ap_without_contacts':float(sensitivity_ap),
              'validation_ap_with_contacts':float(average_precision_score(validation.Churn,val_scores)),
              'caveat':'Unit 1 explored the full snapshot. This is an internal holdout, not an independent external validation or prospective churn forecast.'}
    predictions = pd.DataFrame({'snapshot_row':test.index, 'actual_churn':y,
                                'score':test_scores, 'predicted_churn':(test_scores>=threshold).astype(int)})
    if save:
        OUTPUT.mkdir(exist_ok=True,parents=True)
        (OUTPUT/'model_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        comparison.to_csv(OUTPUT/'model_comparison.csv',index=False)
        threshold_table.to_csv(OUTPUT/'validation_thresholds.csv',index=False)
        importance.to_csv(OUTPUT/'validation_importance.csv',index=False)
        predictions.to_csv(OUTPUT/'test_predictions.csv',index=False)
        assignments = pd.concat([pd.DataFrame({'snapshot_row':x.index,'split':label})
                                for label,x in [('train',train),('validation',validation),('test',test)]])
        assignments.to_csv(OUTPUT/'split_assignments.csv',index=False)
    return result, comparison, importance, predictions

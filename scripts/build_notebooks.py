"""Build the two Unit 2 notebooks; execution is a separate explicit step."""
from pathlib import Path
import nbformat as nbf
ROOT = Path(__file__).resolve().parents[1]

def write(name, cells):
    nb = nbf.v4.new_notebook()
    nb.metadata.kernelspec = {'display_name':'Python 3 (Unit 2)','language':'python','name':'python3'}
    nb.cells = [nbf.v4.new_markdown_cell(text) if kind=='md' else nbf.v4.new_code_cell(text)
                for kind,text in cells]
    nbf.write(nb,ROOT/'jupyter_notebooks'/name)

setup = '''# Resolve paths when launched from either the root or notebook directory.
from pathlib import Path
import sys
ROOT = Path.cwd() if (Path.cwd() / 'src').exists() else Path.cwd().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
from src.data import extract_transform_load, OUTPUT, FEATURES
from src.statistics import wilson_interval, segment_summary, test_hypotheses
plt.rcParams.update({'figure.figsize': (9, 5), 'axes.spines.top': False, 'axes.spines.right': False})
df, quality = extract_transform_load()
print(f'{len(df):,} customer snapshots; {df.Churn.sum():,} attrited ({df.Churn.mean():.2%}).')'''
write('05_unit2_statistics.ipynb',[
('md','''# Unit 2: statistics, probability and exploratory evidence

This extends the Unit 1 credit card analysis for Muhammad Asim. Unit 1 notebooks 01–04 are retained as historical work; this notebook is self-contained from the raw file.

**Audience:** a retention analyst deciding which activity measures deserve further investigation. **Purpose:** quantify recorded attrition and assess three exploratory associations. The snapshot cannot establish which behaviour precedes departure or whether an intervention would work.

## Structured plan and business requirements (LO2.1, LO3.3)

1. Validate and clean the raw customer snapshot using reusable functions.
2. Describe the customer population and uncertainty around observed attrition (BR1).
3. State and test three exploratory hypotheses, report effect sizes and multiple-test adjustment (BR2).
4. Compare activity and product holdings visually (BR2/BR3).
5. Fit and evaluate a classification prototype in notebook 06 (BR4).
6. Present interactive historical segments in the Streamlit dashboard (BR3).
7. Evaluate limitations and record reproducible AI assistance and technical lessons.

The task board and criterion map are in `docs/PROJECT_PLAN.md` and `docs/ASSESSMENT_MAP.md`.'''),
('code',setup),
('md','''## Reproducible ETL and integrity (LO2.1, LO3.1)

`src/data.py` separates validation, transformation and output. Raw data remains unchanged. Validation rejects duplicate/missing identifiers, invalid target labels, missing required fields, nonfinite/negative numerical values, impossible utilisation and fractional counts. A SHA-256 digest records source identity.

The whitelist excludes stored Naive Bayes predictions, the customer identifier and redundant open-to-buy field. Unknown demographic values become missing, without imputation or row deletion. Failure to detect a missingness association does **not** prove missingness is random. Outliers remain because plausible extremes carry information; contact-count tails need small-sample caution. Tenure is retained for historical inspection but excluded from modelling because of a concentration at 36 months of uncertain origin.'''),
('code',"# Inspect the validation record and resulting missingness.\ndisplay(pd.Series(quality, name='Value'))\ndisplay(df.isna().sum().rename('Missing customers').to_frame())"),
('md','''## Core statistical principles (LO1.1 and LO1.2)

- **Mean:** arithmetic average; sensitive to a few large transaction amounts. Useful for portfolio totals and expected workloads.
- **Median:** the middle ordered value; more robust for skewed balances and spending.
- **Variance:** average squared distance from the mean; sample variance uses n−1. **Standard deviation** is its square root and uses the original units.
- **Probability:** the observed fraction attrited estimates P(attrition) for this snapshot. P(attrition | product count) conditions on a segment and uses that segment's denominator. Independence would imply the conditional rates match the unconditional rate.
- **Sampling uncertainty:** Wilson 95% intervals are preferable to a normal approximation near zero or one. The repeated-sampling interpretation is that about 95% of intervals constructed this way cover a fixed population proportion under independent sampling. The file is not proven to be a representative random sample; these intervals do not account for selection bias or future drift.
- **Hypothesis testing:** compare a statistic to its distribution under a null hypothesis. A p-value is not the probability the null is true. Alpha = 0.05 is specified before the Unit 2 tests. Statistical significance alone does not establish practical value or causation.

No normality assumption is imposed on strongly skewed activity variables. Mann–Whitney tests distributional differences; it is not a pure median test unless distributions have the same shape. Rank-biserial effect sizes give signed separation of ranks. Chi-square tests association between product count and outcome; Cramer's V expresses strength on a 0–1 scale.'''),
('code',"# Compare sample mean, median, variance and standard deviation by observed status.\ndescriptive = df.groupby('Attrition_Flag')[['Total_Trans_Ct','Total_Trans_Amt','Total_Revolving_Bal']].agg(['count','mean','median','var','std'])\ndisplay(descriptive.round(3))\nlow, high = wilson_interval(int(df.Churn.sum()), len(df))\nprint(f'P(attrition) = {df.Churn.mean():.4f}; Wilson 95% interval [{low:.4f}, {high:.4f}].')\ndisplay(segment_summary(df,'Total_Relationship_Count'))"),
('md','''## Three exploratory hypotheses (LO3.1)

These follow Unit 1 observations and are therefore **exploratory**, not a new independent confirmatory study.

| Hypothesis | Null hypothesis | Alternative and business question | Method |
|---|---|---|---|
| H1 | Transaction-count distributions are equal between status groups | They differ; does lower observed activity accompany attrition? | Two-sided Mann–Whitney U, rank-biserial effect |
| H2 | Q4/Q1 transaction-count ratio distributions are equal | They differ; is the observed activity change informative? | Two-sided Mann–Whitney U, rank-biserial effect |
| H3 | Product count and attrition are independent | They are associated; which portfolios show greater attrition? | Chi-square and Cramer's V |

Holm correction controls family-wise error across these three tests. It does not remove the exploratory bias from earlier dataset inspection. Rows represent distinct customers, supporting independence between observations; dependence through households/bank processes is unmeasured. We inspect the smallest expected chi-square count before using its asymptotic approximation.'''),
('code',"# Export all test statistics and adjusted p-values for auditability.\nhypotheses = test_hypotheses(df)\nhypotheses.to_csv(OUTPUT / 'hypotheses.csv', index=False)\ndisplay(hypotheses)\nprint('A displayed p=0 is numerical underflow, not literally zero; report p < 0.001.')\nprint('Minimum expected H3 count:', hypotheses.loc[hypotheses.hypothesis.eq('H3'),'minimum_expected_count'].iloc[0])"),
('md','''### Interpretation and practical limits

H1 and H2 show lower activity and count-change ratios in the attrited group, with substantial negative rank-biserial effects. H3 rejects independence but has a smaller Cramer's V. A significant omnibus product-count test does not prove every adjacent product category differs. Segmented rates provide descriptive context only; an experiment is needed to estimate the benefit of selling a third product.

The large sample allows very small p-values. Effect sizes and confidence intervals are more useful for judging the strength and uncertainty of these associations. None of these tests measures lead time.'''),
('code',"# Wilson error bars make small-segment uncertainty visible.\nsummary = segment_summary(df,'Total_Relationship_Count')\nfig, ax = plt.subplots()\nax.bar(summary.Total_Relationship_Count, summary.churn_rate*100, color='#0072B2')\nax.errorbar(summary.Total_Relationship_Count, summary.churn_rate*100,\n yerr=[(summary.churn_rate-summary.ci_lower)*100,(summary.ci_upper-summary.churn_rate)*100],fmt='none',ecolor='#162B3A',capsize=4)\nax.set(xlabel='Products held',ylabel='Recorded attrition (%)',title='Attrition by product portfolio, with 95% Wilson intervals')\nfig.tight_layout()\nfig.savefig(OUTPUT/'product_rates.png',dpi=160)\nplt.show()"),
('code',"# Hexbin counts avoid hiding dense clusters beneath overlapping points.\nfig, axes = plt.subplots(1,2,figsize=(12,4),sharex=True,sharey=True)\nfor ax, status in zip(axes,['Existing Customer','Attrited Customer']):\n group = df[df.Attrition_Flag.eq(status)]\n artist = ax.hexbin(group.Total_Trans_Ct,group.Total_Revolving_Bal,gridsize=25,mincnt=1,cmap='Blues',extent=(0,140,0,2600))\n ax.set(title=f'{status} (n={len(group):,})',xlabel='Annual transaction count')\n fig.colorbar(artist,ax=ax,label='Customers per hexagon')\naxes[0].set_ylabel('Revolving balance ($)')\nfig.suptitle('Activity and balance: within-group concentration, not churn probability')\nfig.tight_layout()\nfig.savefig(OUTPUT/'activity_hexbin.png',dpi=160)\nplt.show()"),
('md','''## Evaluation and next step (LO3.2)

The bar chart maps product holdings to BR2 and includes uncertainty; the hexbin plot maps activity/balance to BR2 while avoiding scatter overplotting. Colour bars are counts with separate scales, so panel intensities cannot be read as comparative churn risk. Neither graphic depends on colour alone: labels identify the groups.

The evidence supports investigating activity-led retention, with human review. Snapshot fields may overlap closure and demographics may be missing for systematic reasons. Avoid claims that inactivity happens first, repeated contacts cause departure or more products prevent it. Notebook 06 evaluates whether these features can classify the recorded status, using a train/validation/test protocol.''')])
write('06_unit2_machine_learning.ipynb',[
('md','''# Unit 2: a reproducible attrition classification prototype

**Defined analytical problem (LO1.3):** classify recorded attrition using ten numerical account activity features. Positive class = attrited customer. **BR4:** compare a useful classifier with a majority baseline, report detection/workload trade-offs and explain the limits of deployment.

This is retrospective snapshot classification. There is no timestamped prediction point or future outcome window. Unit 1 analysed the full dataset; the test split is an internal check within this known dataset, not an independent external validation.'''),
('code',setup),
('md','''## Method selection and exclusions (LO2.2)

Logistic regression offers a scaled, regularised, approximately linear benchmark. A random forest can capture nonlinear activity interactions (for example balance together with transaction count), but is less transparent and can overfit. Compare them with three-fold stratified training cross-validation and select by mean average precision (AP). No broad hyperparameter search is attempted: depth 10, minimum leaf size 5 and 150 trees limit complexity and computation.

A majority classifier supplies the baseline. Accuracy alone is unsuitable: a model predicting everyone retained is already about 84% accurate. AP assesses ranking of the minority class; precision reports how much outreach would be wasted and recall reports how many recorded attrition cases are detected. ROC AUC is supplementary. F2 weights recall more heavily, but has no direct monetary interpretation.

Identifiers, original target text, derived target, stored classifier outputs, redundant open-to-buy, demographics, card category and tenure are excluded from features. Excluding demographics does not establish fairness; behaviour can contain proxies. Closure timing remains a possible source of outcome leakage even after stored predictions are removed.'''),
('code',"# Audit disjoint partitions before training; row numbers are not model features.\nfrom src.modelling import split_data, run_modelling\ntrain, validation, test = split_data(df)\nassert set(train.index).isdisjoint(validation.index)\nassert set(train.index).isdisjoint(test.index)\nassert set(validation.index).isdisjoint(test.index)\ndisplay(pd.DataFrame({'split':['train','validation','test'],'customers':[len(train),len(validation),len(test)],'attrition_rate':[train.Churn.mean(),validation.Churn.mean(),test.Churn.mean()]}))\nprint('Model features:', FEATURES)"),
('md','''## Fitting and decision protocol

1. Make a reproducible stratified 60/20/20 split (seed 42).
2. Fit imputation/scaling **inside each training cross-validation fold** using scikit-learn pipelines. All supplied numerical features are currently complete; a median imputer defines future handling without inventing demographic attributes.
3. Select the model with greatest mean training CV AP, then fit it on the training split.
4. On validation only, choose among thresholds 0.05–0.95 (step 0.025): maximise recall subject to precision ≥60%, then prefer precision and the higher threshold on ties. This floor is an illustrative business constraint because outreach costs are not supplied. If infeasible, the code records that and selects from all candidates.
5. Lock those decisions and evaluate the test split. The model is not refitted on validation/test.
6. Examine validation permutation importance and a validation sensitivity run excluding contacts; these are diagnostics and do not tune test decisions.

Class weighting changes decision scores. Those scores are **not calibrated future churn probabilities**. A random split checks generalisation to similar rows only. Temporal/external validation and calibration assessment would be required for a real forecasting service.'''),
('code',"# Execute the full pipeline from raw data; save metrics, splits and diagnostics.\nresult, comparison, importance, predictions = run_modelling(df)\ndisplay(comparison)\nprint('Selected model:', result['selected_model'])\nprint('Validation precision floor met:',result['validation_precision_floor_met'])\ndisplay(pd.DataFrame([result['test'],result['dummy_test']],index=['Selected test model','Majority baseline']))\nprint('Conditional bootstrap 95% interval for test AP:',result['test_ap_bootstrap_95'])"),
('md','''## Uncertainty and test interpretation (LO3.2)

The AP interval uses 300 bootstrap resamples of test customers with a fixed fitted model. It describes uncertainty conditional on this sample and fitted model. It does not capture retraining variability, prior exploratory selection, bank differences, time drift or the missing prediction window. Cross-validation standard deviation is fold variation, not a confidence interval.

An AP increase over the majority baseline demonstrates better internal ranking of observed statuses. It does not prove that contacted customers can be retained or that a campaign will be profitable.'''),
('code',"# Plot explicit error counts rather than treating accuracy as the sole success criterion.\nr = result['test']\nmatrix = np.array([[r['tn'],r['fp']],[r['fn'],r['tp']]])\nfig, ax = plt.subplots(figsize=(6,4))\nax.imshow(matrix,cmap='Blues')\nfor (i,j), value in np.ndenumerate(matrix):\n ax.text(j,i,str(value),ha='center',va='center',color='white' if value>matrix.max()/2 else '#162B3A')\nax.set(xticks=[0,1],yticks=[0,1],xticklabels=['Retained','Attrited'],yticklabels=['Retained','Attrited'],xlabel='Predicted status',ylabel='Actual status',title='Internal test classification outcomes')\nfig.tight_layout()\nfig.savefig(OUTPUT/'confusion_matrix.png',dpi=160)\nplt.show()\nprint(f\"Detected {r['tp']} of {r['tp']+r['fn']} attrited customers; {r['fp']} false alarms; {r['fn']} missed cases.\")"),
('code',"# Inspect test ranking after the model and threshold have already been locked.\nfrom sklearn.metrics import precision_recall_curve, roc_curve\np, recall, _ = precision_recall_curve(predictions.actual_churn,predictions.score)\nfpr,tpr,_ = roc_curve(predictions.actual_churn,predictions.score)\nfig, axes = plt.subplots(1,2,figsize=(11,4))\naxes[0].plot(recall,p,color='#0072B2')\naxes[0].axhline(predictions.actual_churn.mean(),ls='--',color='#D55E00',label='Prevalence baseline')\naxes[0].set(xlabel='Recall',ylabel='Precision',title='Precision–recall curve'); axes[0].legend()\naxes[1].plot(fpr,tpr,color='#0072B2')\naxes[1].plot([0,1],[0,1],ls='--',color='#D55E00')\naxes[1].set(xlabel='False positive rate',ylabel='True positive rate',title='ROC curve')\nfig.tight_layout()\nfig.savefig(OUTPUT/'model_curves.png',dpi=160)\nplt.show()"),
('code',"# Validation-only reliance and timing sensitivity; neither is a causal explanation.\ndisplay(importance)\nprint('Validation AP with contacts:',result['validation_ap_with_contacts'])\nprint('Validation AP without contacts:',result['validation_ap_without_contacts'])\nthresholds = pd.read_csv(OUTPUT/'validation_thresholds.csv')\nfig, ax = plt.subplots()\nax.plot(thresholds.threshold,thresholds.precision,label='Precision')\nax.plot(thresholds.threshold,thresholds.recall,label='Recall')\nax.axvline(result['test']['threshold'],ls='--',color='#162B3A',label='Selected on validation')\nax.set(xlabel='Decision threshold',ylabel='Score',title='Validation trade-off; no test-set threshold tuning')\nax.legend(); plt.show()"),
('md','''## Recommendations and adaptation (LO3.2, LO4.1, LO4.2)

Use the dashboard for **historical exploration**, not customer eligibility decisions. Activity and portfolio structure warrant further investigation. A production study needs dated features measured before a defined attrition horizon, an external or temporal test, calibration, subgroup error analysis, agreed outreach costs and intervention evidence. Removing contact count barely changes validation AP, so its ambiguous timing is avoidable in a future study; that alone does not solve timing uncertainty in all other activity fields.

This implementation moved from sequential notebook transformations to validated reusable functions and train-only pipelines. Automated guardrails catch duplicate IDs, unexpected labels and invalid values before reports are produced. Hexbin/density views handle overlapping observations more clearly. A separate lean Unit 2 dependency file avoids the legacy profiling helper's installation constraints. These are documented engineering changes, **not a claim about Asim's personal learning**.

Before submission, Asim should review the actual results, run the project himself and complete the personal learning/AI reflection prompts in `docs/LEARNING_REFLECTION.md`. The assistance log records what was actually done and must not be presented as unaided work. Streamlit execution, interaction tests and deployment status are documented in the README.''')])
print('Created Unit 2 notebooks')

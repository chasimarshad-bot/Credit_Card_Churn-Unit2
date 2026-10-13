"""Validate saved model evidence before presenting it to dashboard users."""
import json
import math
import pandas as pd
from .data import FEATURES


def load_model_reports(directory):
    report = json.loads((directory/'model_results.json').read_text(encoding='utf-8'))
    try:
        if report['selected_model'] not in {'Random forest','Logistic regression'}:
            raise ValueError('Unrecognised model name')
        result = report['test']
        for key in ['precision','recall','average_precision']:
            value = result[key]
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f'Invalid model metric: {key}')
        counts = [result[key] for key in ['tn','fp','fn','tp']]
        if any(isinstance(value,bool) or not isinstance(value,int) or value < 0 for value in counts):
            raise ValueError('Invalid classification counts')
        if isinstance(report['split_sizes']['test'],bool) or not isinstance(report['split_sizes']['test'],int) or report['split_sizes']['test'] <= 0 or sum(counts) != report['split_sizes']['test']:
            raise ValueError('Classification counts do not match the test population')
        tn, fp, fn, tp = counts
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        if not math.isclose(result['precision'],precision,abs_tol=1e-12) or not math.isclose(result['recall'],recall,abs_tol=1e-12):
            raise ValueError('Precision or recall disagrees with classification counts')
        baseline = report['dummy_test']['average_precision']
        if isinstance(baseline,bool) or not isinstance(baseline,(int,float)) or not math.isfinite(baseline) or not 0 <= baseline <= 1:
            raise ValueError('Invalid baseline metric')
    except (KeyError,TypeError) as error:
        raise ValueError('Incomplete model evidence') from error
    importance = pd.read_csv(directory/'validation_importance.csv')
    if not {'feature','ap_decrease','sd'}.issubset(importance.columns):
        raise ValueError('Incomplete feature importance report')
    if importance.feature.duplicated().any() or set(importance.feature) != set(FEATURES):
        raise ValueError('Feature importance does not match the model inputs')
    for key in ['ap_decrease','sd']:
        values = pd.to_numeric(importance[key],errors='coerce')
        if not values.map(math.isfinite).all():
            raise ValueError('Invalid feature importance values')
        importance[key] = values
    if importance.sd.lt(0).any():
        raise ValueError('Invalid feature importance variation')
    return report, importance

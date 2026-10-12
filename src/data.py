"""Validated, deterministic ETL for the supplied customer snapshot."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / 'inputs/datasets/raw/BankChurners.csv'
OUTPUT = ROOT / 'outputs/unit2'
FEATURES = ['Total_Relationship_Count', 'Months_Inactive_12_mon',
            'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
            'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
            'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']
DEMOGRAPHICS = ['Customer_Age', 'Gender', 'Dependent_count', 'Education_Level',
                'Marital_Status', 'Income_Category', 'Card_Category', 'Months_on_book']
TARGET_MAP = {'Existing Customer': 0, 'Attrited Customer': 1}


def validate_raw(df):
    """Reject ambiguous targets, repeated customers and invalid numerical domains."""
    required = {'CLIENTNUM', 'Attrition_Flag', *FEATURES, *DEMOGRAPHICS}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    if df.empty or df['CLIENTNUM'].isna().any() or df['CLIENTNUM'].duplicated().any():
        raise ValueError('Expected a nonempty snapshot with unique, nonmissing customer IDs')
    if df['Attrition_Flag'].isna().any() or not set(df['Attrition_Flag']).issubset(TARGET_MAP):
        raise ValueError('Unknown or missing attrition labels')
    if df['Attrition_Flag'].nunique() != 2:
        raise ValueError('Both attrition classes are required')
    numeric = FEATURES + ['Customer_Age', 'Dependent_count', 'Months_on_book']
    for column in numeric:
        values = pd.to_numeric(df[column], errors='coerce')
        if not np.isfinite(values).all() or values.lt(0).any():
            raise ValueError(f'{column} must contain finite, nonnegative numbers')
    if not df['Avg_Utilization_Ratio'].between(0, 1).all():
        raise ValueError('Utilisation must be between zero and one')
    if df['Customer_Age'].lt(18).any():
        raise ValueError('Expected adult customers')
    counts = ['Total_Relationship_Count', 'Months_Inactive_12_mon',
              'Contacts_Count_12_mon', 'Total_Trans_Ct', 'Dependent_count', 'Months_on_book']
    for column in counts:
        if not (df[column] % 1 == 0).all():
            raise ValueError(f'{column} must contain whole counts')
    if df['Months_Inactive_12_mon'].gt(12).any():
        raise ValueError('Annual inactivity cannot exceed 12 months')
    if df['Total_Revolving_Bal'].gt(df['Credit_Limit'] + 0.01).any():
        raise ValueError('Revolving balance exceeds credit limit')
    return df


def clean_data(raw):
    """Whitelist analysis columns; never infer labels or impute demographic facts."""
    validate_raw(raw)
    clean = raw[['Attrition_Flag', *DEMOGRAPHICS, *FEATURES]].copy()
    for column in ['Education_Level', 'Marital_Status', 'Income_Category']:
        clean[column] = clean[column].replace('Unknown', np.nan)
    clean['Churn'] = clean['Attrition_Flag'].map(TARGET_MAP).astype('int8')
    return clean


def load_data(path=RAW_PATH):
    return clean_data(pd.read_csv(path))


def quality_report(raw, clean):
    """Record checks and provenance without persisting customer identifiers."""
    return {'rows_raw': len(raw), 'rows_clean': len(clean),
            'duplicate_ids': int(raw['CLIENTNUM'].duplicated().sum()),
            'churn_count': int(clean['Churn'].sum()),
            'churn_rate': float(clean['Churn'].mean()),
            'missing_values': clean.isna().sum().astype(int).to_dict(),
            'model_features': FEATURES,
            'excluded': ['CLIENTNUM', 'Attrition_Flag', 'Churn', 'Avg_Open_To_Buy',
                         'Naive_Bayes_Classifier_*', *DEMOGRAPHICS]}


def extract_transform_load(path=RAW_PATH):
    import json
    raw = pd.read_csv(path)
    clean = clean_data(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUTPUT / 'customers.csv', index=False)
    report = quality_report(raw, clean)
    report['source_sha256'] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    (OUTPUT / 'quality.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return clean, report

"""Reproduce Unit 2 ETL, hypothesis tests and model evaluation from the raw file."""
from src.data import extract_transform_load, OUTPUT
from src.statistics import test_hypotheses
from src.modelling import run_modelling

if __name__ == '__main__':
    df, report = extract_transform_load()
    tests = test_hypotheses(df)
    tests.to_csv(OUTPUT/'hypotheses.csv',index=False)
    result, _, _, _ = run_modelling(df)
    print(f"Validated {len(df):,} customers; churn {df.Churn.mean():.2%}")
    print(f"Selected: {result['selected_model']}")
    print(result['test'])

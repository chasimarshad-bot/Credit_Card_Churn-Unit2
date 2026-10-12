"""Exploratory hypotheses, effect sizes and uncertainty for the full snapshot."""
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, chi2_contingency, norm


def wilson_interval(successes, total, confidence=0.95):
    """Wilson binomial interval, including zero/all-success samples."""
    if total <= 0:
        return (np.nan, np.nan)
    z = norm.ppf(0.5 + confidence / 2)
    p = successes / total
    denominator = 1 + z*z/total
    middle = (p + z*z/(2*total)) / denominator
    half = z*np.sqrt(p*(1-p)/total + z*z/(4*total*total))/denominator
    return float(middle-half), float(middle+half)


def segment_summary(df, column):
    summary = df.groupby(column, dropna=False, observed=True)['Churn'].agg(
        customers='size', churned='sum', churn_rate='mean').reset_index()
    intervals = [wilson_interval(k, n) for k, n in zip(summary.churned, summary.customers)]
    summary['ci_lower'] = [v[0] for v in intervals]
    summary['ci_upper'] = [v[1] for v in intervals]
    return summary


def test_hypotheses(df):
    """Three two-sided tests with Holm correction; directions interpreted separately."""
    results = []
    for label, column in [('H1', 'Total_Trans_Ct'), ('H2', 'Total_Ct_Chng_Q4_Q1')]:
        left = df.loc[df.Churn.eq(1), column]
        right = df.loc[df.Churn.eq(0), column]
        u, p = mannwhitneyu(left, right, alternative='two-sided', method='asymptotic')
        results.append({'hypothesis': label, 'variable': column, 'test': 'Mann-Whitney U',
                        'statistic': u, 'p_value': p,
                        'effect': 2*u/(len(left)*len(right))-1,
                        'effect_measure': 'rank-biserial (churn minus retained)',
                        'churn_median': left.median(), 'retained_median': right.median()})
    # Preserve all six product counts rather than inventing a threshold after testing.
    table = pd.crosstab(df['Total_Relationship_Count'], df['Churn'])
    chi, p, _, expected = chi2_contingency(table)
    results.append({'hypothesis': 'H3', 'variable': 'Total_Relationship_Count',
                    'test': 'Chi-square independence', 'statistic': chi, 'p_value': p,
                    'effect': np.sqrt(chi/(table.to_numpy().sum()*min(table.shape[0]-1,table.shape[1]-1))),
                    'effect_measure': "Cramer's V", 'minimum_expected_count': expected.min()})
    results = pd.DataFrame(results)
    order = np.argsort(results.p_value.to_numpy())
    adjusted = np.maximum.accumulate([(len(order)-i)*results.p_value.iloc[j]
                                      for i,j in enumerate(order)])
    results['p_holm'] = np.nan
    results.loc[order, 'p_holm'] = np.minimum(adjusted, 1)
    results['reject_at_0_05'] = results.p_holm.lt(0.05)
    return results

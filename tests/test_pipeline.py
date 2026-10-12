"""Meaningful guardrails for data, leakage exclusions, statistics and app interactions."""
import unittest
import numpy as np
import pandas as pd
from src.data import RAW_PATH, FEATURES, clean_data, validate_raw
from src.modelling import split_data, threshold_search
from src.statistics import wilson_interval, test_hypotheses

class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pd.read_csv(RAW_PATH)
        cls.clean = clean_data(cls.raw)

    def test_preserves_rows_and_removes_identifiers_and_leakage(self):
        self.assertEqual(len(self.raw),len(self.clean))
        self.assertEqual(int(self.clean.Churn.sum()),1627)
        self.assertNotIn('CLIENTNUM',self.clean)
        self.assertFalse(any(c.startswith('Naive_Bayes') for c in self.clean))
        self.assertTrue(set(FEATURES).isdisjoint({'Churn','Attrition_Flag','Customer_Age','Months_on_book'}))
        self.assertEqual(int(self.clean.Education_Level.isna().sum()),1519)

    def test_invalid_inputs_fail_instead_of_silent_repair(self):
        cases = []
        cases.append(pd.concat([self.raw,self.raw.iloc[[0]]],ignore_index=True))
        bad = self.raw.copy(); bad.loc[0,'Attrition_Flag']='Other'; cases.append(bad)
        bad = self.raw.copy(); bad.loc[0,'Total_Trans_Ct']=-1; cases.append(bad)
        bad = self.raw.copy(); bad.loc[0,'Credit_Limit']=np.inf; cases.append(bad)
        bad = self.raw.copy(); bad.loc[0,'Avg_Utilization_Ratio']=1.1; cases.append(bad)
        bad = self.raw.copy(); bad['Total_Trans_Ct'] = bad.Total_Trans_Ct.astype(str); cases.append(bad)
        cases.append(self.raw.drop(columns='Total_Trans_Ct'))
        for bad in cases:
            with self.subTest():
                with self.assertRaises(ValueError): validate_raw(bad)

    def test_splits_are_disjoint_complete_and_stratified(self):
        splits = split_data(self.clean)
        indices = [set(d.index) for d in splits]
        self.assertEqual(set.union(*indices),set(self.clean.index))
        for i in range(3):
            self.assertAlmostEqual(splits[i].Churn.mean(),self.clean.Churn.mean(),places=2)
            for j in range(i): self.assertFalse(indices[i] & indices[j])

    def test_wilson_handles_edges_and_uncertainty(self):
        low,high = wilson_interval(0,10)
        self.assertAlmostEqual(low,0)
        self.assertGreater(high,0)
        self.assertGreater(wilson_interval(5,10)[1]-wilson_interval(5,10)[0],
                           wilson_interval(50,100)[1]-wilson_interval(50,100)[0])

    def test_multiple_comparison_correction(self):
        tests = test_hypotheses(self.clean)
        self.assertTrue((tests.p_holm >= tests.p_value).all())
        self.assertTrue(tests.p_holm.between(0,1).all())
        self.assertTrue(tests.loc[tests.hypothesis.eq('H1'),'effect'].iloc[0] < 0)

    def test_threshold_reports_unmet_precision_constraint(self):
        threshold,_,met = threshold_search(pd.Series([0,0,0,1]),np.array([0.5]*4))
        self.assertFalse(met)
        self.assertGreater(threshold,0)

if __name__ == '__main__': unittest.main()

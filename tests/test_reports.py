"""Checks for unavailable or inconsistent saved dashboard evidence."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from src.data import OUTPUT
from src.reports import load_model_reports

class ReportTests(unittest.TestCase):
    def test_valid_saved_reports_load(self):
        report, importance = load_model_reports(OUTPUT)
        self.assertEqual(report['split_sizes']['test'],2026)
        self.assertEqual(len(importance),10)

    def test_inconsistent_counts_or_metrics_are_rejected(self):
        for field, value in [('tp',316),('precision',1.5),('recall',float('nan')),('precision',0.5),('recall',0.5)]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as name:
                folder=Path(name)
                report=json.loads((OUTPUT/'model_results.json').read_text(encoding='utf-8'))
                report['test'][field]=value
                (folder/'model_results.json').write_text(json.dumps(report),encoding='utf-8')
                shutil.copy2(OUTPUT/'validation_importance.csv',folder/'validation_importance.csv')
                with self.assertRaises(ValueError):load_model_reports(folder)

    def test_invalid_baseline_is_rejected(self):
        for value in [True, float('nan'), '0.16', -0.1]:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as name:
                folder=Path(name)
                report=json.loads((OUTPUT/'model_results.json').read_text(encoding='utf-8'))
                report['dummy_test']['average_precision']=value
                (folder/'model_results.json').write_text(json.dumps(report),encoding='utf-8')
                shutil.copy2(OUTPUT/'validation_importance.csv',folder/'validation_importance.csv')
                with self.assertRaises(ValueError):load_model_reports(folder)

    def test_missing_importance_is_reported(self):
        with tempfile.TemporaryDirectory() as name:
            folder=Path(name)
            shutil.copy2(OUTPUT/'model_results.json',folder/'model_results.json')
            with self.assertRaises(FileNotFoundError):load_model_reports(folder)

if __name__ == '__main__':unittest.main()

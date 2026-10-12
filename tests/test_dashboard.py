"""Dashboard smoke tests using Streamlit's supported testing API."""
import unittest
from unittest.mock import patch
import streamlit as st
from streamlit.testing.v1 import AppTest

class DashboardTests(unittest.TestCase):
    def test_filters_empty_reset_missing_and_small_samples(self):
        at = AppTest.from_file('app.py',default_timeout=45).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value,'10,127')
        tables = [table.value for table in at.dataframe]
        frequency = next(table for table in tables if 'Share of status group (%)' in table.columns)
        self.assertEqual(int(frequency.Customers.sum()),10127)
        for share in frequency.groupby('Recorded status')['Share of status group (%)'].sum():
            self.assertAlmostEqual(share,100.0)
        outcomes = next(table for table in tables if 'Predicted retained' in table.columns)
        self.assertEqual(int(outcomes.to_numpy().sum()),2026)
        reliance = next(table for table in tables if 'Activity measure' in table.columns)
        self.assertEqual(len(reliance),10)
        self.assertFalse(reliance['Activity measure'].str.contains('_').any())
        at.multiselect[0].set_value([]).run()
        self.assertFalse(at.exception)
        self.assertTrue(any('No customers' in x.value for x in at.info))
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.multiselect[0].value),4)
        self.assertEqual(at.metric[0].value,'10,127')
        at.checkbox[0].uncheck().run()
        self.assertFalse(at.exception)
        self.assertLess(int(at.metric[0].value.replace(',','')),10127)
        at.button[0].click().run()
        at.multiselect[0].set_value(['Platinum']).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value,'20')
        self.assertTrue(any('Fewer than 30' in x.value for x in at.warning))

    def test_model_report_failure_preserves_portfolio(self):
        st.cache_data.clear()
        try:
            with patch('src.reports.load_model_reports',side_effect=ValueError('Invalid saved evidence')):
                with self.assertLogs(level='ERROR'):
                    at=AppTest.from_file('app.py',default_timeout=45).run()
            self.assertFalse(at.exception)
            self.assertEqual(at.metric[0].value,'10,127')
            self.assertTrue(any('Model review is temporarily unavailable' in item.value for item in at.info))
        finally:
            st.cache_data.clear()

    def test_invalid_source_gives_clear_message(self):
        st.cache_data.clear()
        try:
            with patch('src.data.load_data',side_effect=ValueError('Invalid customer data')):
                with self.assertLogs(level='ERROR'):
                    at=AppTest.from_file('app.py',default_timeout=45).run()
            self.assertFalse(at.exception)
            self.assertTrue(any('customer data is temporarily unavailable' in item.value for item in at.error))
            self.assertEqual(len(at.metric),0)
        finally:
            st.cache_data.clear()

if __name__ == '__main__': unittest.main()

"""Dashboard smoke tests using Streamlit's supported testing API."""
import unittest
from streamlit.testing.v1 import AppTest

class DashboardTests(unittest.TestCase):
    def test_filters_empty_reset_missing_and_small_samples(self):
        at = AppTest.from_file('app.py',default_timeout=45).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value,'10,127')
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

if __name__ == '__main__': unittest.main()

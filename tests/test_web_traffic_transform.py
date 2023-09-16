import os
import sys
import unittest
import pandas as pd

from os.path import dirname
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.web_traffic_transform import process_csv_file
from src.schema_management import map_to_latest_schema

"""
Disclaimer: 

These are some examples of unit tests. Can be used using some actual similar urls or data.
For the assertion of the tests, these will FAIL as they are now with the example data.
Work with the data sources and partners to gather and develop test cases.
"""


class TestWebTrafficTransform(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file content for testing
        self.sample_csv_content = """drop,length,path,user_agent,user_id
                                    False,10,/page1,Chrome,1
                                    True,15,/page2,Firefox,2
                                    False,20,/page1,Chrome,1
                                    False,5,/page3,Edge,2"""

    def test_map_to_latest_schema(self):
        # Define a sample DataFrame with an older schema
        sample_df = pd.DataFrame({'drop': [False, True],
                                   'length': [10, 15],
                                   'path': ['/page1', '/page2'],
                                   'user_agent': ['Chrome', 'Firefox'],
                                   'user_id': [1, 2]})

        # Map to the latest schema and check column names
        result_df = map_to_latest_schema(sample_df, ['drop', 'length', 'path', 'user_agent', 'user_id'])
        expected_columns = ['drop', 'time_spent', 'page_path', 'user_agent', 'user_id']
        self.assertEqual(result_df.columns.tolist(), expected_columns)

    def test_process_csv_file(self):
        # Mock a CSV file URL and process it
        csv_url = "https://example.com/mock.csv"
        user_data = {}
        process_csv_file(csv_url, user_data)

        # Define the expected user data dictionary after processing
        expected_user_data = {
            1: {'/page1': 30},
            2: {'/page2': 15, '/page3': 5}
        }

        self.assertEqual(user_data, expected_user_data)

if __name__ == '__main__':
    unittest.main()
# Define the expected schema for version 2
import os
import sys

from os.path import dirname
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from web_traffic_transform import SCHEMA_V1

SCHEMA_V2 = ['drop', 'time_spent', 'path', 'user_agent', 'user_id']

def validate_schema(dataframe, schema):
    actual_schema = dataframe.columns.tolist()
    if actual_schema != schema:
        raise ValueError(f"Schema mismatch. Expected: {schema}, Actual: {actual_schema}")

def map_to_latest_schema(dataframe, current_schema):
    if current_schema == SCHEMA_V1:
        dataframe.rename(columns={'path': 'page_path', 'length': 'time_spent'}, inplace=True)
    return dataframe
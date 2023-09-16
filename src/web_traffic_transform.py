import os
import sys
import json
import pandas as pd
from io import StringIO
import requests
import logging

from os.path import dirname
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import the functions from the schema_management module
import schema_management as sm

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO or DEBUG as needed.
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='web_traffic_transform.log',  # Specify the log file.
    filemode='a'  # Use 'a' to append to the log file.
)

# Define the expected schema for version 1
SCHEMA_V1 = ['drop', 'length', 'path', 'user_agent', 'user_id']

# Function to read configuration from a file
def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        raise Exception(f"Config file '{config_file}' not found.")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON format in config file '{config_file}'.")


# Function to process data from a CSV file
def process_csv_file(file_url, user_data):
    try:
        # Download CSV file
        response = requests.get(file_url)
        response.raise_for_status()

        # Read data into a DataFrame
        df = pd.read_csv(StringIO(response.text))

        # Log the start of data processing
        logging.info(f"Processing data from {file_url}...")

        # Map to the latest schema version
        df = map_to_latest_schema(df, SCHEMA_V1)

        # Process data and update user_data DataFrame
        df['time_spent'] = df.groupby(['user_id', 'path'])['length'].transform('sum')
        df = df.pivot(index='user_id', columns='path', values='time_spent').fillna(0)

        #user_data = user_data.append(df, sort=False)
        user_data = user_data.add(df, fill_value=0)

        # Log the completion of data processing
        logging.info(f"Data processing from {file_url} completed successfully.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {file_url}: {str(e)}")
    except ValueError as e:
        logging.error(f"Data processing error for {file_url}: {str(e)}")

    return user_data

# Function to validate schema
def validate_schema(df, expected_schema):
    if not all(col in df.columns for col in expected_schema):
        raise ValueError("Schema validation failed. Missing columns in the input data.")

# Function to map schema to the latest version
def map_to_latest_schema(df, current_schema):
    # Mapping logic for schema versions can be added here if needed
    return df

# Main function
def main():
    # Read the configuration file
    config_file = 'config.json'
    config = read_config(config_file)

    # Use the root URL from the config
    url_root = config.get('root_url')
    file_names = [f"{chr(97 + i)}.csv" for i in range(26)]
    user_data = pd.DataFrame(columns=SCHEMA_V1)

    for file_name in file_names:
        file_url = os.path.join(url_root, file_name)
        user_data = process_csv_file(file_url, user_data)

    output_file = config.get('output_file')

    # Write the transformed data to an output CSV file with specified columns
    user_data.to_csv(output_file, index=True, header=True)

if __name__ == '__main__':
    main()
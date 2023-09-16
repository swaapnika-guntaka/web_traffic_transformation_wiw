import boto3
import pandas as pd
from io import StringIO

"""
Disclaimer: 

This code is just meant to be a sample to demonstrate if the data input files are on S3.
Cannot be run. Requires S3 details and credentials in order for this to be functional.
"""

def read_csv_files_from_s3(bucket_name, file_prefix):
    """
    Reads multiple CSV files from an S3 bucket and returns a DataFrame.

    Args:
        bucket_name (str): The name of the S3 bucket.
        file_prefix (str): The prefix for the file names (e.g., folder path).

    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from CSV files.
    """
    # Initialize a Boto3 S3 client
    s3 = boto3.client('s3')

    # List objects in the specified bucket with the given prefix
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=file_prefix)

    # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate through the objects and read CSV files
    for obj in objects.get('Contents', []):
        file_name = obj['Key']
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(content))
        dfs.append(df)

    # Concatenate DataFrames into a single DataFrame
    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        return merged_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no files were found

# Example usage:
bucket_name = 'your-s3-bucket-name'
file_prefix = 'path/to/csv/files/'
data = read_csv_files_from_s3(bucket_name, file_prefix)

# Now 'data' contains the concatenated data from CSV files in the specified S3 bucket and prefix.

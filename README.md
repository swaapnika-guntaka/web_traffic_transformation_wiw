# Web Traffic Data Transformation

## Introduction
This Python script transforms web traffic data from multiple CSV files into a single CSV file, where each row represents a user, and the columns represent the time spent on each page path.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Debugging](#debugging-the-run)
4. [Schema Management](#schema-management)
5. [Data Description](#data-description)
6. [Error Handling](#error-handling)
7. [Unit Tests](#unit-tests)
8. [Best Practices for Future Development](#best-practices-for-future-development)
9. [Impact of Changes](#impact-of-changes)

## Installation
To run the script, follow these steps:
- Clone the repository.
- Install required packages `pip install -r requirements.txt`
- Execute the script using `python web_traffic_transform.py`

## Usage
The script transforms web traffic data from multiple CSV files into a single CSV file. Use it as follows:
- Ensure the data CSV files are accessible.
- Run the script, which will download, process, and transform the data.
- The transformed data will be saved as `output/output.csv`.
- For the purpose of the assignment, the output file is checked into the repo. In order to accurately verify the output, remove the file or remove the contents on the outputfile before running the code.
- `web_traffic_transform_s3.py` is a sample code module if the data input is on s3. This code is not functional currently. Add the right bucket names and credentials to get this running.

## Debugging the Run
- Logs for the run are stored (appended) on `web_traffic_transform.log` file. The file does not need to pre-exist. The code creates the file on the first run and keeps appending the logs from there.
- The log file is a place to start looking when there are issues with the output.
- When running this on cloud, it is a good strategy to save logs on a cloud bucket like S3, for reference in the future.
- Ensure that the lifecycle policies are set so the data is retained as needed. It might easily consume space and hence increase costs.

## Data Description
#(assumed based on understanding. Having a data description is critical for future development and understanding across stakeholders. Gather inputs from the business owners of the data or external sources if its a 3rd party source to document and describe various columns.)
- `drop`: Whether or not this was the last page the user visited before leaving the site.
- `length`: How long the user spent on the page in seconds.
- `path`: The page within the website that the user visited.
- `user_agent`: The browser identifier of the user visiting the page.
- `user_id`: The unique identifier for the user visiting the page.

## Schema Management
- The script manages the schema for data transformation. It supports multiple schema versions and maps columns accordingly.
- Detailed schema management is described in `src/schema_management.py`.

## Error Handling
- The script includes error handling for network errors and data processing errors.
- Error messages provide context for troubleshooting.

## Unit Tests
- Unit tests are available in `tests/test_web_traffic_transform.py`.
- Run tests using `python -m unittest tests/test_web_traffic_transform.py`.

## Best Practices for Future Development
- Code quality and maintainability are emphasized.
- Error handling, documentation, and testing practices are recommended.
- Ensure and add test cases and data quality metrics and extend as needed.

## Impact of Changes
- Schema updates can be critical and can cause failures downstream. Maintain a centralized repository of schemas so users are aware of the changes.
- Maintaining data contracts can be beneficial to seamless integration with downstream systems.
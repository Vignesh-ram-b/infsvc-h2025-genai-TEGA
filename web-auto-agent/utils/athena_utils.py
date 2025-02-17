import boto3
from datetime import datetime

def save_test_result(test_name, status):
    """
    Save test results to AWS Athena.
    """
    athena = boto3.client('athena')
    query = f"""
    INSERT INTO test_results (test_name, status, timestamp)
    VALUES ('{test_name}', '{status}', NOW())
    """
    athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': 's3://my-athena-results/'
        }
    )
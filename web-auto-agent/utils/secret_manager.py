import boto3
import os
from botocore.exceptions import NoCredentialsError

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except NoCredentialsError:
        print("AWS credentials not found.")
        return None

# Example usage
aws_access_key_id = get_secret("AWS_ACCESS_KEY_ID")
aws_secret_access_key = get_secret("AWS_SECRET_ACCESS_KEY")
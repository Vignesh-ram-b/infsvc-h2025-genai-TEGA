import os
import boto3
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_bedrock_client():
    """Initialize and return the Bedrock client."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",  # Replace with your AWS region
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )


def orchestrate_workflow(scenario):
    """
    Generate a base Playwright test script using AWS Bedrock.
    """
    bedrock = get_bedrock_client()
    prompt = f"""
    \n\nHuman: Generate a Playwright test script in Python for the following scenario:
    {scenario}

    The script should:
    1. Keep fixtures for browser, page launch with default view ports and do not add additional fixtures .
    2. Add assertions and retries.
    3. Make sure to add necessary waits in between each actions
    4. Follow Python best practices.

    Return only the Python code. Do not need detailed explanation of what is asked, what is given as response 
    and What needs to be improved details in the response, 
    Needed only python code which should start with imports and end with functions
    Make sure when the script is executed it should handle following:
    1. it should not throw any exception, 
    2. it should not thrown syntax error, 
    3. imports error, 
    4. object has no attribute error, 
    5. AttributeError: 'ElementHandle' object has no attribute 'text'
    6. AttributeError: 'Page' object has no attribute 'wait_for_locator'
    7. AttributeError: 'NoneType' object has no attribute 'locator'
    8. Fixture should not include recursive dependency
    9. Make sure Playwright import is present to avoid 'playwright' not found error
    Final code should be in executable stage
    \n\nAssistant:
    """

    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 1000,
        "temperature": 0.5,
        "top_p": 0.5,
    }

    # body = {
    # "messages": [
    #     {
    #         "role": "user",
    #         "content": prompt
    #     }
    # ],
    # "anthropic_version": "bedrock-2023-05-31",
    # "max_tokens": 1000,
    # "top_k": 250,
    # "stop_sequences": [],
    # "temperature": 1,
    # "top_p": 0.5,
    # }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-v2",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    #print("response_body",response_body["content"][0]["text"])
    return response_body["completion"]
    #return response_body["content"][0]["text"]


def refine_code_with_bedrock(base_script, context):
    """
    Refine generated code using AWS Bedrock.
    """
    bedrock = get_bedrock_client()
    prompt = f"""
    \n\nHuman: Refine the following Playwright test script based on the context below.
    Ensure it includes only browser, page fixtures, proper error handling, and follows best practices.

    Script:
    {base_script}

    Context:
    {context}

    Return only the Python code. Do not need detailed explanation of what is asked, what is given as response 
    and What needs to be improved details in the response, 
    Needed only python code which should start with imports and end with functions
    Make sure when the script is executed it should handle following:
    1. it should not throw any exception, 
    2. it should not thrown syntax error, 
    3. imports error, 
    4. object has no attribute error, 
    5. AttributeError: 'ElementHandle' object has no attribute 'text'
    6. AttributeError: 'Page' object has no attribute 'wait_for_locator'
    7. AttributeError: 'NoneType' object has no attribute 'locator'
    8. Fixture should not include recursive dependency
    9. Keep fixtures for page launch and do not add additional fixtures
    Final code should be in executable stage
    \n\nAssistant:
    """

    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 1000,
        "temperature": 0.5,
        "top_p": 0.5,
    }

    # body = {
    # "messages": [
    #     {
    #         "role": "user",
    #         "content": prompt
    #     }
    # ],
    # "anthropic_version": "bedrock-2023-05-31",
    # "max_tokens": 1000,
    # "top_k": 250,
    # "stop_sequences": [],
    # "temperature": 1,
    # "top_p": 0.5,
    # }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-v2",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    #return response_body["completion"]
    #print("response_body",response_body["content"][0]["text"])
    return response_body["completion"]
    #return response_body["content"][0]["text"]

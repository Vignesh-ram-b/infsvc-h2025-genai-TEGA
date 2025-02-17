import os
from dotenv import load_dotenv
from smol_dev import plan
import openai

# Load environment variables
load_dotenv()

def orchestrate_workflow(scenario):
    """
    Use the `smol-dev` library to generate a workflow or code based on the scenario.
    """
    # Set the OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define a prompt for the smol-dev planner
    prompt = f"""
    Generate a Playwright test script in Python for the following scenario:
    {scenario}

    The script should:
    1. Use the `auto_heal_locator` function to handle dynamic locators.
    2. Include assertions to validate the expected behavior.
    3. Use the `page` object for navigation and interactions.
    4. Handle retries in case of page loading issues.

    Return only the Python code. Does not need detailed explanation of what is asked and what is given as response, 
    Needed only python code which should start with imports and end with functions
    """

    # Use the smol-dev planner to generate the code
    generated_code = plan(prompt)
    return generated_code

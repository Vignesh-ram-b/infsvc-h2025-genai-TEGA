from utils.smol_agent_v2 import orchestrate_workflow
from utils.duckduckgo_tool import search_context
from utils.code_agent import generate_code
import os
import pandas as pd

import re
import os

# def clean_generated_code(refined_script):
#     """
#     Cleans up the generated script by removing markdown-like syntax and explanations.
#     """
#     # Remove markdown-style code blocks
#     refined_script = re.sub(r"```python", "", refined_script)  # Remove starting ```
#     refined_script = re.sub(r"```", "", refined_script)  # Remove ending ```
#
#     # Remove any unnecessary text before/after the actual code
#     refined_script = re.sub(r"Here is the .*?:\n", "", refined_script, flags=re.DOTALL)
#     refined_script = re.sub(r"The key changes:.*", "", refined_script, flags=re.DOTALL)
#
#     return refined_script.strip()

# def generate_test_script(scenario):
#     """
#     Generate a test script dynamically using smol-dev, DuckDuckGo, and Code Agent.
#     """
#     # Use Smol Agent to generate the base script
#     workflow_output = orchestrate_workflow(scenario)
#
#     # Fetch additional context using DuckDuckGo
#     context = search_context(scenario)
#
#     # Use Code Agent to refine the script
#     prompt = f"""
#     Refine the following Playwright test script based on the additional context:
#     {workflow_output}
#
#     Additional context:
#     {context}
#
#     Ensure the script is syntactically correct and follows best practices.
#     """
#     return generate_code(prompt)

from utils.smol_agent_v2 import orchestrate_workflow, refine_code_with_bedrock
from utils.duckduckgo_tool import search_context

import re
import os


def extract_python_code(text):
    match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
    return match.group(1) if match else ""

def clean_generated_script(script_text):
    """
    Cleans the generated script by removing markdown artifacts, explanations, and keeping only valid Python code.
    """
    # Remove markdown markers
    script_text = re.sub(r"```python|```", "", script_text)

    # Remove explanations and bullet points
    script_lines = script_text.split("\n")
    cleaned_lines = []
    inside_code_block = False

    for line in script_lines:
        stripped_line = line.strip()

        # Detect Python function or fixture
        if stripped_line.startswith("def ") or stripped_line.startswith("@pytest.fixture"):
            inside_code_block = True

        # Skip bullet points and explanations
        if not inside_code_block and (stripped_line.startswith("-") or stripped_line.endswith(":")):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

def remove_duplicate_fixtures(test_file_path):
    """
    Removes duplicate fixture and function definitions in a test file.
    """
    if not os.path.exists(test_file_path):
        return

    with open(test_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    fixture_seen = set()
    function_seen = set()
    cleaned_lines = []
    inside_function = False
    function_name = ""

    for line in lines:
        stripped_line = line.strip()

        # Detect fixture functions
        if stripped_line.startswith("@pytest.fixture"):
            inside_function = True
            function_name = stripped_line
            if function_name in fixture_seen:
                continue  # Skip duplicate fixtures
            fixture_seen.add(function_name)

        # Detect function definitions
        if stripped_line.startswith("def "):
            inside_function = True
            function_name = stripped_line.split("(")[0]  # Extract function signature
            if function_name in function_seen:
                continue  # Skip duplicate functions
            function_seen.add(function_name)

        # End of function
        if inside_function and stripped_line == "":
            inside_function = False

        cleaned_lines.append(line)

    # Write cleaned content back to file
    with open(test_file_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

def generate_test_script(scenario, test_name, is_first_test=False):
    """
    Generates a test script, cleans it, and writes/appends it to the test file.
    """
    # Generate base script using Bedrock
    base_script = orchestrate_workflow(scenario)

    # Fetch additional context (optional)
    context = search_context(scenario)

    # Refine the script using Bedrock
    refined_script = refine_code_with_bedrock(base_script, context)

    # Clean the script before saving
    #final_script = clean_generated_script(refined_script)

    refined_script = extract_python_code(refined_script)
    # Define the test file path
    test_file_path = f"tests/test_{test_name}.py"

    # Write to the file: overwrite if it's the first test, append otherwise
    write_mode = "w" if is_first_test else "a"
    with open(test_file_path, write_mode, encoding="utf-8") as file:
        file.write(refined_script + "\n\n")

    # Remove duplicate fixtures after saving
    #remove_duplicate_fixtures(test_file_path)


def process_test_scenarios(file_path):
    """
    Reads test scenarios from an Excel file and generates test files accordingly.
    """
    df = pd.read_excel(file_path)
    grouped_scenarios = df.groupby('test_name')['scenario'].apply(list).to_dict()

    for test_name, scenarios in grouped_scenarios.items():
        for i, scenario in enumerate(scenarios):
            is_first_test = (i == 0)  # First scenario overwrites, others append
            generate_test_script(scenario, test_name, is_first_test)

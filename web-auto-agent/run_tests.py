import json
import os
import pytest
from utils.excel_reader import read_test_scenarios
from utils.test_script_generator import generate_test_script
from utils.report_generator import generate_html_report
from utils.athena_utils import save_test_result

def process_test_scenarios(file_path):
    """
    Reads scenarios from Excel and generates test scripts dynamically.
    """
    test_scenarios = read_test_scenarios(file_path)

    for test_name, scenarios in test_scenarios.items():
        for scenario in scenarios:
            generate_test_script(scenario, test_name)

def generate_and_execute_tests():
    """
    Step 1: Read test scenarios from the Excel file.
    Step 2: Generate test scripts dynamically.
    Step 3: Execute the generated test scripts.
    Step 4: Save test results and generate an HTML report.
    """
    # Step 1: Read test scenarios from Excel
    #scenarios = read_test_scenarios("C:\\Users\\user\\Downloads\\test_scenario_web_ai.xlsx")

    # Step 2: Generate test scripts dynamically
    #generate_test_script(scenarios)

    process_test_scenarios("C:\\Users\\vignesh\\Downloads\\test_scenario_web_ai.xlsx")
    scenarios = read_test_scenarios("C:\\Users\\vignesh\\Downloads\\test_scenario_web_ai.xlsx")

    # Step 3: Execute the generated test scripts
    test_results = []
    for test_name, scenario_list in scenarios.items():
        for i, scenario in enumerate(scenario_list):
            try:
                # Run the specific test function
                #pytest.main([f"tests/test_{test_name}.py", f"-k test_{test_name}_{i}"])
                # pytest.main([
                #     f"tests/test_{test_name}.py",
                #     "--json-report",  # Enable JSON reporting
                #     "--json-report-file=report.json"
                # ])
                # with open("report.json", "r") as file:
                #     report = json.load(file)
                #
                # total_tests = len(report.get("tests", []))
                # passed = sum(1 for test in report.get("tests", []) if test["outcome"] == "passed")
                # failed = sum(1 for test in report.get("tests", []) if test["outcome"] == "failed")
                #
                # print(f"Total Tests: {total_tests}, Passed: {passed}, Failed: {failed}")
                # test_results.append({"test_name": test_name, "scenario": scenario, "status": "Pass"})
                # print(test_results)
                # #save_test_result(test_name, "Pass")
                result = pytest.main([
                    f"tests/test_{test_name}.py"
                   # "-q",  # Quiet mode to reduce console output
                ])

                status = "Pass" if result == 0 else "Fail"
            except Exception as e:
                status = "Fail"
            test_results.append({"test_name": test_name, "scenario": scenario, "status": status})

    print(json.dumps(test_results, indent=4))
        # test_results.append({"test_name": test_name, "scenario": scenario, "status": status})
        #     except Exception as e:
        #         test_results.append({"test_name": test_name, "scenario": scenario, "status": "Fail"})
        #         #save_test_result(test_name, "Fail")

    # Step 4: Generate HTML report
    generate_html_report(test_results)

if __name__ == "__main__":
    generate_and_execute_tests()

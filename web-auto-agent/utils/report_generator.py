def generate_html_report(test_results):
    """
    Generate an HTML report dynamically based on the test results.
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Report</title>
    </head>
    <body>
        <h1>Test Results</h1>
        <table border="1">
            <tr>
                <th>Test Name</th>
                <th>Scenario</th>
                <th>Status</th>
            </tr>
    """

    for result in test_results:
        html += f"""
        <tr>
            <td>{result['test_name']}</td>
            <td>{result['scenario']}</td>
            <td>{result['status']}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    with open("artifacts/reports/report.html", "w") as file:
        file.write(html)
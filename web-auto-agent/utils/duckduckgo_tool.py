# from duckduckgo_search import DDGS
#
#
# # def search_context(query):
# #     results = DDGS(query, max_results=3)
# #     return results
#
# def search_context(query, max_results=10):
#     with DDGS() as ddgs:
#         return ddgs.text(query, max_results=max_results)

from duckduckgo_search import DDGS


# def format_query(test_cases):
#     """Converts a dictionary of test cases into a readable search query."""
#     return " ".join([" ".join(v) for v in test_cases.values()])
#
#
# def search_context(query, max_results=10):
#     with DDGS() as ddgs:
#         query=format_query(query)
#         print(query)
#         results = ddgs.text(query, max_results=max_results)
#     return results

from duckduckgo_search import DDGS

def format_query(scenario_str):
    """
    Convert scenario string into a search-friendly query.
    Example: "Login with valid credentials" -> "Login+with+valid+credentials"
    """
    # Split into keywords and join with '+' for URL encoding
    return "+".join(scenario_str.strip().split())

def search_context(scenario):
    """
    Search DuckDuckGo for additional context about the test scenario.
    Returns first 3 search results as context.
    """
    try:
        with DDGS() as ddgs:
            query = format_query(scenario)
            results = ddgs.text(query, max_results=3)
            return "\n".join([result["body"] for result in results])
    except Exception as e:
            print(f"Search failed: {str(e)}")
            return "No additional context available."

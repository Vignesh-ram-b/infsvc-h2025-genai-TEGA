# from playwright.sync_api import sync_playwright
# import time
#
# def auto_heal_locator(page, element_description, retries=3):
#     for attempt in range(retries):
#         try:
#             page.wait_for_selector(element_description, timeout=5000)
#             return element_description
#         except:
#             if attempt == retries - 1:
#                 raise
#             time.sleep(2)  # Wait before retrying

from playwright.sync_api import sync_playwright
import openai

def auto_heal_locator(page, element_description):
    try:
        # Try to find the element using the original locator
        page.wait_for_selector(element_description, timeout=5000)
        return element_description
    except:
        # If not found, use generative AI to suggest a new locator
        prompt = f"Suggest a Playwright locator for the element: {element_description} on the page: {page.content()}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        new_locator = response.choices[0].text.strip()
        return new_locator

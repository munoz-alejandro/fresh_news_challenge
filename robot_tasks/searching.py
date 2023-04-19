from .utils import get_variable
from RPA.Browser.Selenium import Selenium

def search_news(browser: Selenium):
    """
    This function searches for news articles using a web browser and a search term.

    :param browser: The web browser object that is being used to interact with the webpage
    :param term: The search term that the function will use to search for news articles
    """
    # Variables
    term = get_variable("search")
    search_button = '//button[contains(@class, "css-tkwi90")]'
    search_input = '//input[@data-testid="search-input"]'
    search_submit = '//button[@data-test-id="search-submit"]'

    # Actions
    browser.click_element(search_button)
    browser.input_text_when_element_is_visible(search_input, term)
    browser.click_element_when_visible(search_submit)
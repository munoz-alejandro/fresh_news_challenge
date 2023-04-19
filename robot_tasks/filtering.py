import sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException)
from selenium.webdriver.common.by import By

from RPA.Browser.Selenium import Selenium

from .utils import get_variable, accept_cookies

def generic_apply_filter(
        browser: Selenium,
        options: list,
        selected_items: list,
        type: str
        ):
    """
    This function applies a filter to a web browser based on selected items and a type.

    :param browser: The browser object that is being used to interact with the web page
    :param options: It is a list of all the available options that can be selected in the filter
    :param selected_items: It seems like the parameter `selected_items` is a list of items that have
    been selected by the user. The function `generic_apply_filter` takes this list along with other
    parameters such as `browser`, `options`, and `type` to apply a filter on a webpage. The function
    first finds
    :param type: The type parameter is a string that specifies the type of filter to apply. It is used
    to identify the button that needs to be clicked to open the filter options
    """

    button = get_type_or_section_button(type)
    found_items = list(set(selected_items).intersection(options))
    browser.click_button(button)

    for item in found_items:
        input = f"//label[@class='css-1a8ayg6']//span[contains(text(), '{str(item)}')]"
        browser.click_element(input)


def get_type_or_section_button(type: str):
    """
    The function returns a button xpath based on the input type.

    :param type: The parameter "type" is a string that specifies whether the button is for a section or
    a type. If the value of "type" is "section", the function returns the XPath for the button under the
    section category. If the value of "type" is anything else, the function returns the
    :return: an XPath string for a button element based on the input parameter "type". If the input
    parameter is "section", the XPath string returned is for a button element within a div with a
    data-testid attribute equal to "section". If the input parameter is not "section", the XPath string
    returned is for a button element within a div with a data-testid attribute equal to "type".
    """
    if type == "section":
        button = '//div[@data-testid="section"]//button'
    else:
        button = '//div[@data-testid="type"]//button'
    return button



def generic_get_values_from_ul(browser: Selenium, type: str):
    """
    This function retrieves values from a specific type of unordered list (ul) element on a webpage
    using Selenium.

    :param browser: The Selenium browser object used to interact with the web page
    :type browser: Selenium
    :param type: The "type" parameter is a string that specifies the type of section to retrieve values
    from. It is used to locate and click the corresponding button before retrieving the values
    :type type: str
    :return: a list of strings, which are the text values of the sections obtained from an unordered
    list (ul) element on a web page. The function uses Selenium to interact with the web page and
    extract the text values.
    """
    button = get_type_or_section_button(type)
    browser.click_button(button)

    li_span_text = "//ul[@class='css-64f9ga']//span[@class='css-16eo56s']"
    li_span_news_qty = ".//span[@class='css-17fq56o']"

    section = browser.get_webelements(li_span_text)

    sections = []

    # iter WebElements
    for item in section:
        try:
            # Get hole span text
            browser.wait_until_element_is_visible(item)
            span_text = browser.get_text(item)
            # Get news qty in text
            news_qty = item.find_element(By.XPATH, li_span_news_qty)
            browser.wait_until_element_is_visible(news_qty)
            news_qty_text = browser.get_text(news_qty)
            # Remove the news qty from the text
            text = span_text.replace(news_qty_text, '')
            # Append the text to response
            sections.append(text)
        except NoSuchElementException:
            print(f"this span ({span_text}) doesn't have news qty")
            sections.append(span_text)
        except StaleElementReferenceException as e:
            print(e)

    return sections


def get_search_months(month):
    """
    This function returns the start and end dates for a search period of either 1 or 2 months ago.
    :return: A dictionary containing the start and end dates for a search period. The start and end
    dates are formatted as strings in the format "mm/dd/yyyy". The length of the search period is
    determined by the value of the variable "search_months", which is set to 2 by default but can be
    changed. If "search_months" is 0, the search period is set to 1 month.
    """
    month = int(month)
    if month < 0:
        sys.exit("month can be lower than 0")

    search_months = 1 if month == 0 else month

    end_date = date.today()

    """
    Today date is april 18:
    if search_month = 0 or 1 then start date is april 1 and end date is today
    search_month = 2 start date is march 1 and end date is today
    search_month = 3 start date is feb 1 and end date is today
    + 3 keeps working like that month 3 or 2
    """
    if search_months == 1:
        start_date = datetime(end_date.year, end_date.month, 1)
    else:
        substract_months = search_months-1
        start_date = end_date - relativedelta(months=substract_months)
        start_date = datetime(start_date.year, start_date.month, 1)

    end_date = end_date.strftime("%m/%d/%Y")
    start_date = start_date.strftime("%m/%d/%Y")

    return {"start":start_date, "end":end_date}


def set_recent_news(browser: Selenium):
    """
    This function sets the sorting option for recent news articles in a web browser.

    :param browser: The browser parameter is likely an instance of a web browser object, such as
    Selenium's WebDriver, that is being used to automate interactions with a web page
    """
    value = "newest"
    sort_select_element = '//select[@data-testid="SearchForm-sortBy"]'
    browser.select_from_list_by_value(sort_select_element, value)


def filter_news_by_dates(browser: Selenium, month: str):
    """
    This function filters news articles by specific dates using a web browser.

    :param browser: The browser object represents the web browser being used to interact with a website.
    It is likely an instance of a web driver such as Selenium
    """
    # Variables
    button = '//button[@data-testid="search-date-dropdown-a"]'
    specific_dates_button = '//button[@type="button"][text()="Specific Dates"]'
    start_date = '//input[@data-testid="DateRange-startDate"]'
    end_date = '//input[@data-testid="DateRange-endDate"]'
    date_ranges = get_search_months(month)

    #Actions
    browser.click_button(button)
    browser.click_button_when_visible(specific_dates_button)
    browser.input_text_when_element_is_visible(start_date, date_ranges["start"])
    browser.input_text_when_element_is_visible(end_date, date_ranges["end"])
    browser.press_keys(end_date, "ENTER")


def determine_type_or_section(news_section, news_type, options):
    """
    The function determines whether to filter news articles by section or type based on the available
    options.

    :param news_section: It is a list of strings representing the available news sections (e.g.
    "politics", "sports", "entertainment")
    :param news_type: This parameter is a list of all the types of news articles available, such as
    "politics", "sports", "entertainment", etc
    :param options: The list of options that the user has selected to filter the news articles. It could
    contain one or more sections or types of news articles, or just the string "Any" if the user has not
    selected any specific filter
    :return: a string indicating whether to filter by news section or news type based on the available
    options. The function returns "section" if there are more options available for news sections,
    "type" if there are more options available for news types, and "section" if the number of options
    available for both news sections and news types are equal.
    """
    # default if only "Any" is in list
    if options == ["Any"]:
        return "section"

    # find sections or types found in available options
    sections_found = list(set(options).intersection(news_section))
    types_found = list(set(options).intersection(news_type))

    # count found results
    count_types = len(types_found)
    count_sections = len(sections_found)

    # compare who has more found items to determine the filters to apply
    if count_types > count_sections:
        return "type"

    if count_sections > count_types:
        return "section"

    # if equals default to section
    if count_sections == count_types:
        return "section"


def filter_category_news(browser):
    selections = get_variable("category_or_section")
    month = get_variable("months")

    accept_cookies(browser)

    filter_news_by_dates(browser, month)
    set_recent_news(browser)

    news_sections = generic_get_values_from_ul(browser, "section")
    news_types = generic_get_values_from_ul(browser, "type")

    selections_count = len(selections)
    if selections_count == 0:
        selections = ["Any"]

    type_or_section = determine_type_or_section(
            news_sections,
            news_types,
            selections
        )

    if type_or_section == "section":
        generic_apply_filter(browser, news_sections, selections, type_or_section)

    if type_or_section == "type":
        generic_apply_filter(browser, news_types, selections, type_or_section)
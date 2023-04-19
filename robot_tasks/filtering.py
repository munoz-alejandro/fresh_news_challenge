from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import sys

def generic_apply_filter(browser, options, selected_items, type):
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


def get_type_or_section_button(type):
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



def generic_get_values_from_ul(browser, type):
    """
    This function retrieves values from a specific type of unordered list (ul) on a webpage using a web
    browser object.

    :param browser: The web browser object used to interact with the webpage
    :param type: The type parameter is a string that represents the type of section to retrieve values
    from. It is used to locate and click the corresponding button on the webpage
    :return: a list of section names extracted from a web page using the provided browser object and a
    specified type.
    """

    button = get_type_or_section_button(type)
    browser.click_button(button)

    li_span = "//ul[@class='css-64f9ga']//label/span"
    li_news_number_span = "//ul[@class='css-64f9ga']//label/span/span"

    section = browser.get_webelements(li_span)
    section_number_count = browser.get_webelements(li_news_number_span)

    news_number, sections = [], []

    for item in section_number_count:
        text = browser.get_text(item)
        news_number.append(text)

    counter = 0
    for item in section:
        text = browser.get_text(item)
        if counter != 0:
            text_to_remove = str(news_number[counter-1])
            text = text.replace(text_to_remove, '')
        sections.append(text)

        counter = counter + 1
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


def set_recent_news(browser):
    """
    This function sets the sorting option for recent news articles in a web browser.
    
    :param browser: The browser parameter is likely an instance of a web browser object, such as
    Selenium's WebDriver, that is being used to automate interactions with a web page
    """
    value = "newest"
    sort_select_element = '//select[@data-testid="SearchForm-sortBy"]'
    browser.select_from_list_by_value(sort_select_element, value)


def filter_news_by_dates(browser, month):
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


def filter_category_news(browser, sections, categories, month):

    filter_news_by_dates(browser, month)
    set_recent_news(browser)

    news_sections = generic_get_values_from_ul(browser, "section")
    news_types = generic_get_values_from_ul(browser, "type")

    sections_count = len(sections)
    categories_count = len(categories)

    if sections_count == 0 and categories_count == 0:
        sections = ["Any"]
        categories = ["Any"]
        generic_apply_filter(browser, news_sections, sections, "section")
        generic_apply_filter(browser, news_types, categories, "type")
    elif sections_count > categories_count:
        generic_apply_filter(browser, news_sections, sections, "section")
    elif categories_count > sections_count:
        generic_apply_filter(browser, news_types, categories, "type")
    else:
        generic_apply_filter(browser, news_sections, sections, "section")
import os
from datetime import datetime
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Browser.Selenium import Selenium
import logging

def get_output_path() -> str:
    """
    This function returns the absolute path of the "output" directory located in the parent directory of
    the current file.
    :return: the absolute path to the "output" directory, which is a subdirectory of the parent
    directory of the directory where the current Python script is located.
    """
    #instance dirname
    path_to_save = "output"

    #instance dirname
    dirname=os.path.dirname

    # get absolute root path
    base_path = os.path.abspath(dirname(dirname((__file__))))
    output_dir = os.path.join(base_path, path_to_save)

    return output_dir

def clean_image_url(image_url: str) -> str:
    """
    The function takes an image URL and returns only the filename by removing the domain and any query
    parameters.

    :param image_url: The URL of an image that needs to be cleaned to extract only the filename
    :type image_url: str
    :return: The function `clean_image_url` takes a string `image_url` as input and returns a string
    `filename`. The `filename` is obtained by extracting the last part of the `image_url` after
    splitting it by `/` and removing any query parameters by splitting it by `?`. The function returns
    the `filename`.
    """
    # image_url like
    # https://static01.nyt.com/ai-high-stakes-illo-threeByTwoSmallAt2X.png?quality=75

    if image_url == "N/A":
        return image_url

    # get only the filename, removing domain and in server path
    filename = image_url.split('/')[-1]
    # remove the get parameters
    filename = filename.split('?')[0]

    return filename



def get_variable(name: str) -> str:
    """
    This function retrieves defined variables from WorkItems.

    :param name: The name of the variable that we want to retrieve from the work item
    :type name: str
    :return: the value of the variable with the given name that is stored in the current work item.
    """
    wi = WorkItems()
    wi.get_input_work_item()

    variable = wi.get_work_item_variable(name)

    return variable

def get_screenshot_path() -> str:
    """
    This function returns the path to the "screenshots" folder within the output path.
    :return: a string representing the path to the "screenshots" directory within the output directory.
    """
    output_path = get_output_path()
    screenshots = "screenshots"
    path = os.path.join(output_path, screenshots)

    return path

def get_screenshot_name() -> str:
    """
    This function generates a filename for a screenshot with the current date and time and saves it in a
    specified output path.
    :return: The function `get_screenshot_name()` returns a string representing the filename of a
    screenshot image file. The filename includes the current date and time in the format
    "screenshot_DDMMYYYY_HHMMSS_page.png", where "DD" represents the day, "MM" represents the month,
    "YYYY" represents the year, "HH" represents the hour, "MM" represents the minute,
    """
    path = get_output_path()
    now = datetime.now()
    now_str = now.strftime("%d%m%Y_%H%M%S")
    filename = "screenshot_"+now_str+"_page.png"

    filename = os.path.join(path, filename)

    return filename

def accept_cookies(browser: Selenium) ->  None:
    """
    This function accepts cookies on a webpage using Selenium.

    :param browser: The parameter "browser" is an instance of the Selenium class, which is used to
    automate web browsers for testing and web scraping purposes. It allows the script to interact with
    the web page and perform actions such as clicking buttons, filling out forms, and navigating through
    pages
    :type browser: Selenium
    """
    accept_button = "//button[@data-testid='GDPR-accept']"
    try:
        browser.page_should_contain_element(accept_button)
        browser.click_button(accept_button)
        browser.reload_page()
    except AssertionError:
        logging.error("Can't find cookies button")
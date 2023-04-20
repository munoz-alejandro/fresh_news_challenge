from .utils import get_output_path, get_screenshot_path

import os, shutil, sys
import logging

from RPA.Robocorp.WorkItems import WorkItems
from RPA.Browser.Selenium import Selenium



def configure_browser() -> Selenium:
    """
    This function configures a Selenium browser instance with a specified screenshot path.
    :return: an instance of the Selenium class, which has been configured with a screenshot path.
    """
    # Set screenshot path
    screenshot_path = get_screenshot_path()
    browser = Selenium(screenshot_root_directory=screenshot_path)
    return browser

def open_site(browser: Selenium) -> None:
    """
    Opens the New York Times website in an available web browser.
    """
    logging.INFO("Starting [general][open_site]")
    url = 'https://www.nytimes.com/'
    browser.open_available_browser(url)
    logging.INFO("Ending [general][open_site]")

def close_browser_instance(browser: Selenium) -> None:
    """
    Close the browser instance
    """
    logging.INFO("Starting [general][close_browser_instance]")
    browser.close_browser
    logging.INFO("Starting [general][close_browser_instance]")

def check_path_and_clean(path) -> None:
    """
    This function checks if a directory exists, and if it does, it deletes all files and subdirectories
    within it, otherwise it creates the directory.

    :param path: The path parameter is a string that represents the directory path that needs to be
    checked or created
    """
    # check if path exists
    if os.path.exists(path):
        # if path exists it cleans the folder
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            # identify if is file or directory and try to delete it
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            # except there is an error
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        # else it creates the directory
        os.mkdir(path)

def check_excel_files(path):
    """
    This function cleans excel files in a specified directory by deleting them.

    :param path: The parameter "path" is a string that represents the directory path where the function
    will look for Excel files to clean
    """
    # cleans excel files in the output directory
    for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            # identify if is file or directory and try to delete it
            if ".xlsx" in str(filename):
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                # except there is an error
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

def check_variables() -> None:
    """
    The function checks if three required variables are present in a Work Item and exits the program if
    they are not.
    """
    try:
        wi = WorkItems()
        wi.get_input_work_item()

        SEARCH = wi.get_work_item_variable("search")
        CATEGORY_OR_SECTION = wi.get_work_item_variable("category_or_section")
        MONTHS = wi.get_work_item_variable("months")
    except KeyError as e:
        print("This robot needs 3 variables to run: search, category_or_section and months")
        print(e)
        sys.exit("Please add it as Work Item in the Control Room")

def init_process() -> Selenium:
    """
    The function performs checks on the output path, including checking the images directory and Excel
    files. Also initialize the browser instance and return it
    """
    logging.INFO("Starting [general][init_process]")
    browser = configure_browser()
    check_variables()
    output_path = get_output_path()
    images_path = os.path.join(output_path, "images")
    screenshots_path = os.path.join(output_path, "screenshots")
    check_path_and_clean(screenshots_path)
    check_path_and_clean(images_path)
    check_excel_files(output_path)

    logging.INFO("Ending [general][init_process]")
    return browser
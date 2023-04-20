
from SeleniumLibrary.errors import ElementNotFound

from RPA.Browser.Selenium import Selenium

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    NoSuchElementException)

import logging

def get_all_results(browser: Selenium):
    """
    The function clicks on a "show more" button on a webpage until the button is no longer present.

    :param browser: The browser object that is being used to interact with a web page
    """
    show_more_button = "//button[@data-testid='search-show-more-button']"
    main_xpath = "//li[@data-testid='search-bodega-result']"
    counter = 1
    condition = True
    url = browser.get_location()
    current_news = 0
    while condition:
        try:
            news_qty = browser.get_element_count(main_xpath)
            browser.location_should_be(url)
            browser.page_should_contain_element(show_more_button)

            #Prevents unnecesary cliks
            if news_qty != current_news:
                browser.wait_until_element_is_visible(show_more_button)
                counter = counter+1
                current_news = news_qty
            else:
                current_news = current_news + 1
                continue
        except AssertionError as e:
            if "Location should have been" in repr(e):
                print("Incorrect location, reloading page")
                browser.go_back()
                counter = 1
            else:
                print("Page doesn't have show more button")
                condition = False
        except ElementClickInterceptedException as e:
            # print("Element 'show_more_button' is not clickable. Other element would receive the click")
            print(e)
            browser.reload_page()
            counter = 1
            current_news = 0
        except StaleElementReferenceException:
            """
            For some reason the element was marked as invalid and we should restart this process.
            """
            print("stale element reference: element is not attached to the page document")
            print("realoading page and starting again")
            browser.reload_page()
            counter = 1
        except ElementNotFound:
            """
            Sometimes the element can't be found after the iterations
            """
            print("Element can't be found")
            browser.reload_page()


def get_new_image(browser: Selenium, new: WebElement):
    """
    This function takes a Selenium browser and an image element, attempts to retrieve the image source
    attribute, and returns a dictionary with the image source and a boolean indicating whether the image
    was found.

    :param browser: Selenium - a Python library used for automating web browsers
    :type browser: Selenium
    :param image_element: WebElement is an object that represents an HTML element on a web page. In this
    case, the image_element parameter is a WebElement object that represents an image element on a web
    page. It is used to extract the source URL of the image
    :type image_element: WebElement
    :return: A dictionary containing the image source and a boolean indicating whether the image was
    found or not.
    """
    image_found = False
    try:
        image_element = new.find_element(By.XPATH, ".//img[@class='css-rq4mmj']")
        image = browser.get_element_attribute(image_element, "src")
        image_found = True
    except NoSuchElementException as e:
        image = "N/A"
    return {"image": image, "found":image_found}

def get_new_description(browser: Selenium, new: WebElement) -> None:
    """
    This function retrieves the text from a web element and returns it along with a boolean indicating
    whether the element was found.

    :param browser: Selenium is a Python library used for automating web browsers. In this code, it is
    being used to interact with a web page
    :type browser: Selenium
    :param description_element: WebElement is an object that represents an HTML element on a web page.
    In this case, the "description_element" parameter is a WebElement object that represents the element
    on the web page that contains the description text that we want to extract. This element could be a
    paragraph, a div, or any other
    :type description_element: WebElement
    :return: A dictionary containing the description text and a boolean indicating whether the
    description was found or not.
    """
    description_found = False
    try:
        description_element = new.find_element(By.XPATH, ".//p[@class='css-16nhkrn']")
        description = browser.get_text(description_element)
        description_found = True
    except NoSuchElementException as e:
        description = "N/A"
    return {"description": description, "found":description_found}


def get_data_from_entries(browser: Selenium):
    """
    This function extracts data from a webpage using XPaths and returns a list of news data.

    :param browser: The browser object is an instance of a web driver that allows the script to interact
    with a web page
    :param search: The search parameter is a string that represents the search query that will be used
    to search for news articles on a website
    :return: a list of lists containing the title, date, and description of news articles obtained from
    a web page using XPaths.
    """
    main_xpath = "//li[@data-testid='search-bodega-result']"
    descriptions_xpath = '//li[@data-testid="search-bodega-result"]//p[@class="css-16nhkrn"]'
    images_xpath = "//li[@data-testid='search-bodega-result']//img"

    news_count = browser.get_element_count(main_xpath)
    images_count = browser.get_element_count(images_xpath)
    descriptions_count = browser.get_element_count(descriptions_xpath)

    news = browser.get_webelements(main_xpath)
    print(news_count)

    print(f"There are {news_count-images_count} less images than news")
    print(f"There are {news_count-descriptions_count} less descriptions than news")

    news_data = []
    for new in range(news_count):
        current_new = news[new]

        title_element = current_new.find_element(By.XPATH, ".//h4")
        date_element = current_new.find_element(By.XPATH, ".//span[@data-testid='todays-date']")

        image = get_new_image(browser, current_new)
        description = get_new_description(browser, current_new)
        title = browser.get_text(title_element)
        date = browser.get_text(date_element)
        new_data = [title, date, description["description"], image["image"]]
        if new_data not in news_data:
            news_data.append([title, date, description["description"], image["image"]])

    print(len(news_data))
    return news_data

def get_news_data(browser: Selenium):
    """
    This function expands all news and retrieves data including title, date, description, and image from
    entries using a Selenium browser.

    :param browser: The parameter "browser" is an instance of the Selenium webdriver that is being used
    to automate the web browser. It is passed as an argument to the function "get_news_data" so that the
    function can interact with the web page and extract the necessary data
    :type browser: Selenium
    :return: The function `get_news_data` returns a list of news data, where each news item is
    represented as a list containing the following information: title, date, description, and image.
    """

    logging.INFO("Starting [scraping][get_news_data]")
    get_all_results(browser)

    # data information contains
    # 0 title | 1 date | 2 description | 3 image
    data = get_data_from_entries(browser)

    logging.INFO("Starting [scraping][get_news_data]")
    return data
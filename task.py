from RPA.Browser.Selenium import Selenium
import os

from robot_tasks.general import open_site, close_browser_instance, perform_checks
from robot_tasks.searching import search_news
from robot_tasks.filtering import filter_category_news
from robot_tasks.scraping import get_news_data
from robot_tasks.excel import create_file
from robot_tasks.calculations import get_calculated_data
from robot_tasks.downloading import download_images


if __name__ == "__main__":

    env = perform_checks()

    search = env["search"]
    sections = env["sections"]
    categories = env["categories"]
    months = env["months"]

    browser = Selenium()
    open_site(browser)
    search_news(browser, search)
    filter_category_news(browser, sections, categories, months)
    data = get_news_data(browser)
    data_with_extra_info, images_data = get_calculated_data(data, search)
    create_file(data_with_extra_info, search)
    download_images(images_data)
    close_browser_instance(browser)
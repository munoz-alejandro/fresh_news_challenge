import logging

from robot_tasks.utils import get_screenshot_name
from robot_tasks.general import open_site, close_browser_instance, init_process
from robot_tasks.searching import search_news
from robot_tasks.filtering import filter_category_news
from robot_tasks.scraping import get_news_data
from robot_tasks.excel import create_file
from robot_tasks.calculations import get_calculated_data
from robot_tasks.downloading import download_images

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    try:
        browser = init_process()
        open_site(browser)
        search_news(browser)
        filter_category_news(browser)
        data = get_news_data(browser)
        data_with_extra_info, images_data = get_calculated_data(data)
        create_file(data_with_extra_info)
        download_images(images_data)
        close_browser_instance(browser)
    except Exception as e:
        filename = get_screenshot_name()
        browser.capture_page_screenshot(filename=filename)
        logging.ERROR(e)

from .utils import get_output_path
import os, shutil, sys, json

def open_site(browser):
    """
    Opens the New York Times website in an available web browser.
    """
    url = 'https://www.nytimes.com/'
    browser.open_available_browser(url)

def close_browser_instance(browser):
    """
    Close the browser instance
    """
    browser.close_browser

def check_images_directory(path):
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


def get_env_variables():
    #try:
    search = os.environ["SEARCH"]
    months = os.environ["MONTHS"]
    sections_txt = os.environ["SECTIONS"].replace(
            ' , ', ', '
        ).replace(
            ' ,', ', '
        ).replace(
            ', ', ','
        )
    sections =  sections_txt.split(",")
    categories_txt = os.environ["CATEGORIES"].replace(
            ' , ', ', '
        ).replace(
            ' ,', ', '
        ).replace(
            ', ', ','
        )
    categories =  categories_txt.split(",")

    return {
        'search': search,
        'months': months,
        'sections': sections,
        'categories': categories
    }


def perform_checks():
    """
    The function performs checks on the output path, including checking the images directory and Excel
    files.
    """
    env = get_env_variables()
    output_path = get_output_path()
    images_path = os.path.join(output_path, "images")
    check_images_directory(images_path)
    check_excel_files(output_path)

    return env
import os
from datetime import datetime
from RPA.Robocorp.WorkItems import WorkItems

def get_output_path():
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

def clean_image_url(image_url: str):
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



def get_variable(name: str):
    wi = WorkItems()
    wi.get_input_work_item()

    variable = wi.get_work_item_variable(name)

    return variable

def get_screenshot_path():
    output_path = get_output_path()
    screenshots = "screenshots"
    path = os.path.join(output_path, screenshots)

    return path

def get_screenshot_name():
    path = get_screenshot_path()
    now = datetime.now()
    now_str = now.strftime("%d%m%Y_%H%M%S")
    filename = "screenshot_"+now_str+"_page.png"

    filename = os.path.join(path, filename)

    return filename


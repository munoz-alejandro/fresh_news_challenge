import os

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

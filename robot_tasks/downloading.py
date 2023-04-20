import requests
import os
import shutil
import logging

from .utils import get_output_path


def count_items_in_directory(path):
    """
    The function counts the number of files in a given directory path.

    :param path: The path parameter is a string that represents the directory path for which we want to
    count the number of files
    :return: the count of files in the directory specified by the `path` parameter.
    """
    count = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            count += 1

    return count

def download(data, image_folder):
    """
    The function downloads images from URLs in a given data set and saves them to a specified folder.

    :param data: The data parameter is a list of lists, where each inner list contains information about
    an image to be downloaded. The first element of each inner list is the filename to be used for the
    downloaded image, and the second element is the URL where the image can be found
    :param image_folder: The image_folder parameter is a string representing the path to the folder
    where the downloaded images will be saved
    """
    for row in data:
        filename = row[0]
        image_url = row[1]
        if image_url != "N/A":
            # img buffer
            img_data = requests.get(image_url).content
            # output / filename
            file_path = os.path.join(image_folder, filename)
            # save the image to the given path
            with open(file_path, 'wb') as handler:
                handler.write(img_data)

def zip_images(output_path: str, directory: str) -> None:
    filename = os.path.join(output_path, "images")
    shutil.make_archive(filename, 'zip', directory)

def download_images(data: list):
    """
    This function downloads a list of images from URLs and saves them to a specified output path.

    :param data: A list of tuples containing the name and URL of images to be downloaded. The first
    element of each tuple is the image name and the second element is the image URL
    :type data: list
    """
    logging.info("Starting [downloading][download_images]")
    #  0 image name | 1 image url
    output_path = get_output_path()
    image_folder = os.path.join(output_path, 'images')
    img_qty = 0
    items_downloaded = 0

    condition = True

    tries = 3

    while condition:
        # get quantity of images to download
        img_qty = len(data)

        # if images to download are zero, finish the execution
        if img_qty == 0:
            condition = False

        # if images aren't equal to the items downloaded, it tries to download the files
        if img_qty != items_downloaded:
            download(data, image_folder)
            tries = tries-1

        # get a fresh count of items downloaded
        items_downloaded = count_items_in_directory(image_folder)

        # if images are equal to the items downloaded, it finish the execution
        if img_qty == items_downloaded:
            condition = False

        # Avoid infinite loop if after 3 intents it can't download all images
        if tries == 0:
            condition = False

    zip_images(output_path, image_folder)
    logging.info("Ending [downloading][download_images]")
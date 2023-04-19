import re
from .utils import clean_image_url, get_variable

def find_money_in_text(text: str):
    """
    The function `find_money_in_text` uses regular expressions to check if a given text contains a valid
    money format.

    :param text: The input text that we want to search for money values
    :type text: str
    :return: The function `find_money_in_text` returns a boolean value indicating whether the input
    `text` contains a valid money format or not.
    """
    pattern = re.compile('|'.join([
        r'\$[\d,]+(\.\d{1,2})?( USD| dollars)?',
        r'\$\d+',
        r'(\b\d+\s+dollars\b)|(\b\d+\s+USD\b)'
    ]))

    result = pattern.search(text)
    found = result is not None

    return found

def count_search_phrases(text: str, search: str):
    # Does not include overlapping matches
    # Case insensitive
    count = text.lower().count(search.lower())
    return count


def get_calculated_data(data: list):
    """
    The function takes a list of data and adds extra information to each item in the list, including
    whether the text contains money and the count of search phrases.

    :param data: The input parameter is a list of lists, where each inner list contains information
    about a particular item. The inner lists have four elements: title, date, description, and image
    :type data: list
    :return: The function `get_calculated_data` is returning a list of lists. Each inner list contains
    the original data passed in as an argument (title, date, description, and image), as well as two
    additional pieces of information: whether the text (title and description concatenated) contains
    money (as determined by the `find_money_in_text` function) and the count of search phrases in the
    text (as determined by the `count_search_phrases` function)
    """

    search = get_variable("search")
    # data information contains
    # 0 title | 1 date | 2 description | 3 image

    data_with_extra_info = []
    # for control
    unique_images = []
    # to actually store images information (url and name)
    images_data = []
    for new in data:
        # concatenate title and description
        text = new[0]+new[2]
        contains_money = find_money_in_text(text)
        search_phrases = count_search_phrases(text, search)
        image_name = clean_image_url(new[3])
        # data_with_extra_info information contains
        # 0 title | 1 date | 2 description | 3 image name
        # 4 contains money | 5 count search phrases
        data_with_extra_info.append([
            new[0],
            new[1],
            new[2],
            image_name,
            contains_money,
            search_phrases
            ])

        if image_name not in unique_images and image_name != "N/A":
            unique_images.append(image_name)
            images_data.append([image_name, new[3]])

    print(len(data_with_extra_info))

    return data_with_extra_info, images_data




import os, logging
from datetime import datetime

from openpyxl import Workbook

from .utils import get_output_path, get_variable


class CreateWorkbook:
    def __init__(
        self,
        data,
        search
    ):
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.data = data
        self.search = search

    def write_headers(self):
        """
        This function writes a list of headers to a worksheet in a spreadsheet.
        """
        headers = [
            'title',
            'date',
            'description',
            'image name',
            'contains money',
            'count search phrase'
            ]

        self.worksheet.append(headers)

    def set_title(self):
        """
        This function sets the title of a worksheet to a string representation of a search term.
        """
        self.worksheet.title = str(self.search)

    def write_content(self):
        """
        The function writes the data in rows to a worksheet.
        """
        # 0 title | 1 date | 2 description | 3 image name
        # 4 image_url | 5 contains money | 6 count search phrases
        for row in self.data:
            self.worksheet.append(row)


    def save_document(self):
        """
        This function saves a workbook as an Excel file in a specified directory.

        :param file_name: The name of the file to be saved. If no name is provided, the default name
        "searching_results.xlsx" will be used, defaults to searching_results.xlsx (optional)
        """

        today= datetime.now()
        today_str= today.strftime("%m_%d_%Y__%H_%M_%S")
        file_name= f"searching_results_{today_str}.xlsx"

        output_path = get_output_path()
        final_path = os.path.join(output_path, file_name)

        self.workbook.save(final_path)

    def create_excel_file(self):
        """
        This function creates an Excel file by setting the title, writing headers and content, and
        saving the document.
        """
        self.set_title()
        self.write_headers()
        self.write_content()
        self.save_document()

def create_file(data):
    logging.info("Starting [excel][create_file]")
    search = get_variable("search")
    create_workbook = CreateWorkbook(data, search)
    create_workbook.create_excel_file()
    logging.info("Starting [excel][create_file]")
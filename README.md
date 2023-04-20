# New York Times Web Scraper Bot

This web scraper bot is made with Robot Framework in Python and is designed to scrape the New York Times web page and store the news in an Excel file and the news images in a zip file.

## Requirements

To use this web scraper bot, you will need the following:

- Python 3.6 or later
- Follow the guide to start working with bots in VS Code [Guide](https://robocorp.com/docs/courses/beginners-course/set-up-robocorp-lab)
- You will also need to download the latest version of ChromeDriver and add it to your system path. You can download it from the following link: https://chromedriver.chromium.org/downloads

## Usage

To use this web scraper bot, follow these steps:

1. Clone this repository to your local machine.
2. Open a terminal window and navigate to the project directory.
3. Run the following command to open the directory in VS Code:
> code .
4. Configure your search terms in `devdata/work-items-in/search-news/work-items.json`
4. Ctrl + Shift + P in Windows or Linux, Cmd + Shift + P in Mac and then `> Robocorp: Run Robot`.
5. The bot will scrape the latest news articles and their images, and store them in an Excel file and a zip file, respectively.
6. Once the bot has finished scraping, you will see the results in the `output/` directory.

## Customization

If you want to customize the web scraper bot, you can do so by modifying the `task.py` file and the code inside `robot_tasks/`. You can change the dates of news articles to scrape, the sections or types and the term to search in `devdata/work-items-in/search-news/work-items.json` or in the Control Room inside robocorp.

## License

This web scraper bot is licensed under the Apache License, Version 2.0. See the `LICENSE` file for more information.

## Acknowledgements

This web scraper bot was created by Alejandro Muñoz. It uses the Robot Framework, Selenium Library for Robot Framework, and OpenPyXL Library. The New York Times web page is used for demonstration purposes only.
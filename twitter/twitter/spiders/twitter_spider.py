import scrapy
import re
import time
import os
from bs4 import BeautifulSoup
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# There is an output.csv tracing the results, kindly reminder to check it.
class TwitterMentionsSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ["twitter.com"]
    start_urls = [
        'https://twitter.com/Mr_Derivatives',
        'https://twitter.com/warrior_0719',
        'https://twitter.com/ChartingProdigy',
        'https://twitter.com/allstarcharts',
        'https://twitter.com/yuriymatso',
        'https://twitter.com/TriggerTrades',
        'https://twitter.com/AdamMancini4',
        'https://twitter.com/CordovaTrades',
        'https://twitter.com/Barchart',
        'https://twitter.com/RoyLMattox'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 10,  # Set the delay between requests to 10 seconds
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_ARGUMENTS': ['--start-maximized']
    }

    def start_requests(self):
        os.environ['SELENIUM_DRIVER_EXECUTABLE_PATH'] = 'C:/Users/youss/Downloads/chromedriver-win64/chromedriver.exe'
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        time.sleep(10)  # Wait for 10 seconds before parsing

        # Get the Selenium driver
        driver = response.meta['driver']

        # Send END key press event 3 times with a 5-second delay
        # Because the Data isn't returning I'm trying to refresh the page to search for $cashing
        for _ in range(3):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(5)

        # Get the page source using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tweets = soup.find_all('div', class_='css-901oao css-bfa6kz r-m0bqgq r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-bcqeeo r-qvutc0')

        # Counting the number of mentions
        counter = 0
        for tweet in tweets:
            text = tweet.text
            if re.search(r'\$[A-Za-z]{3,4}', text):
                counter += 1

        yield {
            'url': response.url,
            'mentions': counter
        }

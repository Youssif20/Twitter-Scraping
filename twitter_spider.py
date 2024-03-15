import scrapy
from scrapy_selenium import SeleniumRequest
import time
import os


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
        # Extracting text from the specified XPath
        text = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "r-1ye8kvj", " " ))]').extract()

        # Counting the number of mentions of '$TSLA'
        counter = sum(1 for mention in text if '$TSLA' in mention)

        yield {
            'url': response.url,
            'tsla_mentions': counter
        }


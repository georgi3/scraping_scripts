import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.service import Service
from shutil import which
import time


class NavigationSpider(scrapy.Spider):
    name = 'navigation'
    allowed_domains = ['duckduckgo.com']
    start_urls = [
        'http://duckduckgo.com/',
    ]

    def __init__(self):
        CHROME_DRIVER_PATH = which('chromedriver')
        options = Options()
        options.binary_location = '/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome'
        # options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
        # driver.set_window_size(2560, 1600)
        driver.get('https://duckduckgo.com')
        time.sleep(4)
        search_box = driver.find_element(By.XPATH, "(//div[@class='searchbox_searchbox__eaWKL']/input)[3]")
        search_box.send_keys('My User Agent')
        time.sleep(4)
        search_box.send_keys(Keys.ENTER)
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for article in resp.xpath('//div[@class="ikg2IXiCD14iVX7AdZo1"]'):
            yield {
                'article': article.xpath('.//h2/a/span/text()').get(),
                'article_link': article.xpath('.//h2/a/@href').get()
            }

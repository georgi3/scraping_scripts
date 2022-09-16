import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from scrapy.http.response import html
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.duckduckgo.com',
            wait_time=3,
            screenshot=False,
            callback=self.parse,

        )

    def parse(self, response: html.HtmlResponse):
        # img = response.meta['screenshot']
        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        driver = response.meta['driver']
        search_input = driver.find_element(By.XPATH, '//input[@id="search_form_input_homepage"]')
        search_input.send_keys('Hello World')
        search_input.send_keys(Keys.ENTER)

        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath('//div[@class="result__extras__url"]/a')
        for link in links:
            yield {
                'article': link.xpath('.//@href').get(),
                # 'article_link': article.xpath('.//a/@href').get()
            }


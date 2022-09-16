import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    url = 'https://slickdeals.net'
    # allowed_domains = ['slickdeals.net']
    # start_urls = ['http://slickdeals.net/']

    def start_requests(self):
        yield SeleniumRequest(
            url=self.url+'/computer-deals/',
            wait_time=3,
            callback=self.parse,
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 '
                              'Mobile Safari/537.36 '
            }
        )

    def parse(self, response):
        products = response.xpath('//ul[@class="dealTiles categoryGridDeals blueprint"]/li')
        for product in products:
            yield {
                'name': product.xpath('.//a[contains(@class, "itemTitle")]/text()').get(),
                'link': self.url+product.xpath('//a[contains(@class, "itemTitle")]/@href').get(),
                'store_name': product.xpath('normalize-space(.//button[contains(@class, "itemStore")]/text())').get(),
                'price': product.xpath('normalize-space(.//div[contains(@class, "itemPrice")]/text())').get(),
            }
        next_page = response.xpath('//a[@data-role="next-page"]/@href').get()
        next_page = None
        if next_page:
            abs_url = f'{self.url}{next_page}'
            print(f"""
            LINK 
            
            {abs_url}
            """)
            yield SeleniumRequest(
                url=abs_url,
                wait_time=3,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 '
                                  'Mobile Safari/537.36 '
                }
            )

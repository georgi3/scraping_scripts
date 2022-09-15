import scrapy
from scrapy.http.response import html
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response: html.HtmlResponse):
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
            yield response.follow(url=response.urljoin(link),
                                  callback=self.parse_country,
                                  meta={'country_name': name})

    def parse_country(self, response: html.HtmlResponse):
        # logging.info(response.url)
        name = response.request.meta['country_name']
        rows = response.xpath(query='(//table[@class="table table-striped table-bordered table-hover table-condensed '
                                    'table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath(query='.//td[1]/text()').get()
            population = row.xpath(query='.//td[2]/strong/text()').get()
            yield {
                'name': name,
                'year': year,
                'population': population
            }


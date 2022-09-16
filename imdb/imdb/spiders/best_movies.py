import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.response import html


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/104.0.5112.102 Mobile Safari/537.36 '

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating',
                             headers={
                                 'User-Agent': self.user_agent
                             })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True,
             process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[1]'),
             process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response: html.HtmlResponse):
        yield {
            'title': response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').get(),
            'year': response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI '
                                   'baseAlt"]/li[1]/a/text()').get(),
            'duration': ''.join(response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers '
                                               'sc-8c396aa2-0 kqWovI baseAlt"]/li[3]/text()').getall()),
            'genre': response.xpath('(//div[@class="ipc-chip-list__scroller"])[1]/a/span/text()').get(),
            'rating': response.xpath('(//div[@class="sc-7ab21ed2-2 kYEdvH"])[2]/span[1]/text()').get()+'/10',
            'movie_url': response.url,
            # 'user': response.request.headers['User-Agent']
        }

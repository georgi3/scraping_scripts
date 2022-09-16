import scrapy
import json
from scrapy.exceptions import CloseSpider


class EbooksSpider(scrapy.Spider):
    name = 'ebooks'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12']
    INCREMENT = 12
    offset = 0

    def parse(self, response):
        if response.status == 500:
            CloseSpider('Reached last page...')
        resp = json.loads(response.body)
        ebooks = resp.get('works')
        for book in ebooks:
            print(f"""
'title': {book.get('title'),}
'subject': {book.get('subject')}
            """)
            yield {
                'title': book.get('title'),
                'subject': book.get('subject')
            }

        self.offset += self.INCREMENT
        yield scrapy.Request(
            url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
            callback=self.parse
        )

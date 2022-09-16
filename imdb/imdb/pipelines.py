# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3


class ImdbPipelineSQL:
    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get('MONGO_URI'))
    #     return cls()

    def open_spider(self, spider):
        self.connection = sqlite3.connect('imdb.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS imdb250(
        title TEXT,
        year TEXT,
        duration TEXT,
        genre TEXT,
        rating TEXT,
        movie_url TEXT
        )
        
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
        INSERT INTO imdb250 (title, year, duration, genre, rating, movie_url)
        VALUES (?,?,?,?,?,?)
        """, (
            item.get('title'),
            item.get('year'),
            item.get('duration'),
            item.get('genre'),
            item.get('rating'),
            item.get('movie_url'),
        ))
        self.connection.commit()

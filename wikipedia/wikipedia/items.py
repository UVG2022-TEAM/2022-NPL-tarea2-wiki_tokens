# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikipediaItem(scrapy.Item):
    parrafo = scrapy.Field()


# class TokenText(scrapy.Item):
#    text = scrapy.Field()
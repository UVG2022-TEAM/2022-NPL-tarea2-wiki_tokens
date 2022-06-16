import scrapy
from scrapy.shell import inspect_response
from wikipedia.items import TokenText

class wikiSpider(scrapy.Spider):
    name = 'wiki_tokens'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    def parse(self, response):
        i = 0
        for link in response.css('.featured_article_metadata > a'):
            yield response.follow(link.attrib.get('href'), callback=self.parse_article_data)
            i += 1
            if i == 5: #Solo leer el primer link
                break

    def parse_article_data(self, response):
        text = ''
        text_content = response.css('#mw-content-text')
        for par in text_content.css('.mw-parser-output > p'): #Read all p from the body of the article
            text += ' '.join(par.css('*::text').getall())

        yield TokenText (
            text = text
        )
        
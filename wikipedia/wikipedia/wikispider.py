import scrapy
from scrapy.shell import inspect_response
from wikipedia.items import TokenText

class wikiSpider(scrapy.Spider):
    name = 'wiki_tokens'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']


    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'file:C://Users//wchavarria//OneDrive - Comunicaciones Celulares, S.A//Analytics//sample-code//maestria_data_science//nlp//tarea_scrappy//fran-%(time)s.json'
        #'CLOSESPIDER_ITEMCOUNT': 20
    }

    def parse(self, response):
        i = 0
        for link in response.css('.featured_article_metadata > a'):
            yield response.follow(link.attrib.get('href'), callback=self.parse_article_data)
            i += 1
            if i == 1: #Solo leer el primer link
                break

    def parse_article_data(self, response):
        text = ''
        text_content = response.css('#mw-content-text')
        for par in text_content.css('.mw-parser-output > p'): #Read all p from the body of the article
            text += ' '.join(par.css('*::text').getall())

        yield TokenText(
            text = text
        )
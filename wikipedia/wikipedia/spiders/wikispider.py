import scrapy
import re
import unihandecode
import pipe
from collections import Counter
import matplotlib.pyplot as plt
from pipe import select
from wikipedia.items import WikipediaItem

class wikiSpider(scrapy.Spider):
    name = 'wiki_tokens'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']


    #custom_settings = {
        #'FEED_FORMAT': 'json',
        #'FEED_URI': 'file:C://Users//wchavarria//OneDrive - Comunicaciones Celulares, S.A//Analytics//sample-code//maestria_data_science//nlp//tarea_scrappy//fran-%(time)s.json'
        #'CLOSESPIDER_ITEMCOUNT': 20
    #}

    def parse(self, response):
        i = 0
        for link in response.css('.featured_article_metadata > a'):
            yield response.follow(link.attrib.get('href'), callback=self.parse_article_data)
            i += 1
            if i == 5: # Solo leer el primer link
                break

    def parse_article_data(self, response):

        def conv(org_list, seperator=' '):
            return seperator.join(org_list).lower()

        contenido = response.xpath('/html/body')
        for parrafo in contenido:
            lista_parrafo_grande = parrafo.xpath('//p//text()').getall()
            sin_unicode = list(lista_parrafo_grande | select(lambda x: unihandecode.unidecode(x)))
            sin_especial = [re.sub('[^a-zA-Z0-9]+|[\]\[\b\d+\b]', ' ', _) for _ in sin_unicode]
            sin_espacios = list(sin_especial | select(lambda x: x.strip()))
            sin_blancos = [x for x in sin_espacios if x]
            sin_dobles = [re.sub(r' +', ' ', string) for string in sin_blancos]
            parrafo_grande = conv(sin_dobles)

        yield {
                'texto': parrafo_grande
            }

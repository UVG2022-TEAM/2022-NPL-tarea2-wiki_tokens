import scrapy
import re
import unihandecode
import pipe
from collections import Counter
import matplotlib.pyplot as plt
from pipe import select
from wikipedia.items import WikipediaItem
from bs4 import BeautifulSoup

class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['es.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']
        #'https://es.wikipedia.org/wiki/Crisis_ruso-ucraniana_de_2021-2022'
        #'https://es.wikipedia.org/wiki/Presidencia_de_Donald_Trump'
    #]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'file:C://Users//wchavarria//OneDrive - Comunicaciones Celulares, S.A//Analytics//sample-code//maestria_data_science//nlp//tarea_scrappy//wiki-%(time)s.json'
        #'CLOSESPIDER_ITEMCOUNT': 20
    }


    def parse(self, response):
        host = self.allowed_domains[0]
        lits = response.css(".featured_article_metadata a::attr(href)")
        for i, href in enumerate(lits):
            yield response.follow(href, callback=self.parse_vinculo)
            if(i >= 24):
                break   
        
    def parse_vinculo(self, response):
        base_url = 'en.wikipedia.org/wiki'
        contenido = response.xpath('/html/body')
        for parrafo in contenido:
            x = parrafo.xpath('.//div/h1/text()').get().replace(" ", "_")
            parx = cleantext = BeautifulSoup(parrafo.xpath('.//div/p[2]').get(), "lxml").text
            yield {
                'link': f"https://{base_url}{'/'}{x}",
                'body': {
                    'title': parrafo.xpath('.//div/h1/text()').get(),
                    'paragraph': parx
                }
            }
                

        # contenido = response.xpath('/html/body')
        # for parrafo in contenido:
        #     # item = WikipediaItem()
        #     lista_parrafo_grande = parrafo.xpath('//p//text()').getall()
        #     sin_unicode = list(lista_parrafo_grande | select(lambda x: unihandecode.unidecode(x)))
        #     sin_especial = [re.sub('[^a-zA-Z0-9]+|[\]\[\b\d+\b]', ' ', _) for _ in sin_unicode]
        #     sin_espacios = list(sin_especial | select(lambda x: x.strip()))
        #     sin_blancos = [x for x in sin_espacios if x]
        #     sin_dobles = [re.sub(r' +', ' ', string) for string in sin_blancos]
        #     parrafo_grande = conv(sin_dobles)
           
        #     yield {
        #         'texto': parrafo_grande
        #     }
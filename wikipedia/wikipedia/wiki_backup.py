import scrapy
import re
import unihandecode
import pipe
from collections import Counter
import matplotlib.pyplot as plt
from pipe import select
from wikipedia.items import WikipediaItem


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['es.wikipedia.org']
    start_urls = [
        'https://es.wikipedia.org/wiki/Crisis_ruso-ucraniana_de_2021-2022',
        'https://es.wikipedia.org/wiki/Presidencia_de_Donald_Trump',
        'https://es.wikipedia.org/wiki/Conquista_del_Pet%C3%A9n',
        'https://es.wikipedia.org/wiki/Cultura_maya',
        'https://es.wikipedia.org/wiki/Michael_Jackson',
        'https://es.wikipedia.org/wiki/Armada_bizantina',
        'https://es.wikipedia.org/wiki/P%C3%ADo_XII',
        'https://es.wikipedia.org/wiki/Proyecto_Manhattan',
        'https://es.wikipedia.org/wiki/Elvis_Presley'
    ]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'file:C://Users//wchavarria//OneDrive - Comunicaciones Celulares, S.A//Analytics//sample-code//maestria_data_science//nlp//tarea_scrappy//wiki-%(time)s.json'
        #'CLOSESPIDER_ITEMCOUNT': 20
    }


    def parse(self, response):

        def conv(org_list, seperator=' '):
            return seperator.join(org_list).lower()

        contenido = response.xpath('/html/body')
        for parrafo in contenido:
            # item = WikipediaItem()
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
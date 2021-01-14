import scrapy


class BmwParser(scrapy.Spider):
    name = 'bmw_parser'

    start_urls = [
        'https://auto.ru/moskva/cars/bmw/used/'
    ]



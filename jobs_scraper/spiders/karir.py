# -*- coding: utf-8 -*-
import scrapy


class KarirSpider(scrapy.Spider):
    name = 'karir'
    allowed_domains = ['karir.com']
    start_urls = ['http://karir.com/search']

    def parse(self, response):
        pass

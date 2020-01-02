# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    field = scrapy.Field()
    company = scrapy.Field()
    image = scrapy.Field()
    location = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    url = scrapy.Field()
    posting_date = scrapy.Field()
    closing_date = scrapy.Field()
    description = scrapy.Field()

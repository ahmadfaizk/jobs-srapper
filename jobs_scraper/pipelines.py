# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests

class JobsScraperPipeline(object):
    def process_item(self, item, spider):
        job = {
            'name': item['title'],
            'company': item['company'],
            'image': item['image'],
            'location': item['location'],
            'field': item['field'],
            'source': 2,
            'min_salary': item['min_salary'],
            'max_salary': item['max_salary'],
            'posting_date': item['posting_date'],
            'closing_date': item['closing_date'],
            'url': item['url'],
            'description': item['description']
        }
        response = requests.post('http://localhost:8000/api/v1/crawl', data=job, headers={'Accept': 'Application/json'})
        print(response.json())
        return item

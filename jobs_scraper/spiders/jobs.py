# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import JobsScraperItem

bulan = ['January', 'February', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'December']
regex_url = r'https://www.jobs.id/\w+/\w+/[\w-]+'
page_limit = 239
page_count = 0
job_count = 0

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['jobs.id']
    start_urls = ['https://www.jobs.id/lowongan-kerja']

    def parse(self, response):
        list_jobs = response.css('div.single-job-ads')
        for job in list_jobs:
            url = job.css('h3 a').xpath('@href').get()
            url = re.findall(regex_url, url)[0]
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        url = 'https://www.jobs.id'
        url += response.xpath('//a[@rel="next"]/@href').get()
        url = response.urljoin(url)
        global page_count
        page_count += 1
        if page_count < page_limit:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_detail(self, response):
        item = JobsScraperItem()
        global job_count
        job_count += 1
        item['index'] = job_count
        item['title'] = response.css('h1::text').get().strip()
        item['company'] = parceCompany(response.css('h5 a strong::text'))
        item['location'] = parseLocaton(response.css('span.location::text'))
        item['field'] = response.css('h4 a.cyan::text').get()
        item['image'] = parseImage(response.css('div.company-profile img'))
        gaji = response.css('h4 span::text').re(r'[\d.]+')
        item['min_salary'] = parseGaji(gaji, 0)
        item['max_salary'] = parseGaji(gaji, 1)
        item['posting_date'] = parseDate(response.css('p.text-gray::text').get().strip())
        item['closing_date'] = parseDate(response.css('p.text-gray.text-right::text').get().strip())
        item['url'] = response.request.url
        item['description'] = parseDetail(response)
        return item

def parseDate(date):
    date = date.split()
    tgl = date[2]
    bln = str(bulan.index(date[3])+1)
    thn = date[4]
    return thn + "-" + bln + "-" + tgl

def parseGaji(gaji, index):
    if len(gaji):
        return int(gaji[index].replace('.', ''))
    else:
        return 0

def parseDetail(response):
    desc = response.xpath('//div[@class="job_desc"]//text()').re(r'[\S ]+')
    req = response.xpath('//div[@class="job_req"]//text()').re(r'[\S ]+')
    if len(desc):
        desc = "Deskripsi Pekerjaan\r\n" + "\r\n".join(desc) + "\r\n\n"
    else:
        desc = ""
    if len(req):    
        req = "Persyaratan\r\n" + "\r\n".join(req)
    else:
        req = ""
    text =  desc + req
    return text.strip()

def parseImage(response):
    if (response.get()):
        return 'https:' + response.xpath('@src').get()
    else:
        return 'https://cdn04.jobs.id/asset/images/company_default.png'

def parceCompany(response):
    if response.get():
        return response.get()
    else:
        return 'Perusahaan Dirahasiakan'

def parseLocaton(response):
    arr = response.get().split()
    index = len(arr) - 1
    if arr[index] == 'dan':
        return response.get().replace('dan', '').strip()
    else:
        return response.get().strip()
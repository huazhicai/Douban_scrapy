# -*- coding: utf-8 -*-
import scrapy


class AqispiderSpider(scrapy.Spider):
    name = 'aqispider'
    allowed_domains = ['www.aqistudy.cn']
    start_urls = ['http://www.aqistudy.cn/']

    def parse(self, response):
        pass

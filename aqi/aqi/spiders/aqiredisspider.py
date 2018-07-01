# -*- coding: utf-8 -*-
import scrapy


class AqiredisspiderSpider(scrapy.Spider):
    name = 'aqiredisspider'
    allowed_domains = ['www.aqistudy.cn']
    start_urls = ['http://www.aqistudy.cn/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopingItem(scrapy.Item):
    # define the fields for your item here like:
    job_title = scrapy.Field()
    job_link = scrapy.Field()
    job_info = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()

    # 增加爬虫名称和时间戳
    crawled = scrapy.Field()
    spider = scrapy.Field()

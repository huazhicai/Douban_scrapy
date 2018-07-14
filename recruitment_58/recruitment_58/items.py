# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class IndustryUrlItem(Item):
    url = Field()   # 行业电销招聘网址


class Recruitment58Item(Item):
    # define the fields for your item here like:
    title = Field()     # 招聘标题
    salary = Field()    # 薪水
    company = Field()   # 公司名称
    website = Field()   # 公司简介网址

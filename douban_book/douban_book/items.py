# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubanBookCategoryItem(Item):
    # define the fields for your item here like:
    categoty = Field()      # 分类
    tag = Field()           # 标签
    url = Field()           # 标签链接
    num = Field()           # 数量
    pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


# movie item
class Top250MovieItem(Item):
    # define the fields for your item here like:
    ranking = Field()
    poster = Field()
    title = Field()
    alias = Field()
    link = Field()
    star = Field()
    info = Field()
    describe = Field()
    pass


# music item
class Top250MusicItem(Item):
    poster = Field()
    title = Field()
    link = Field()
    author = Field()
    time = Field()
    star = Field()
    pass



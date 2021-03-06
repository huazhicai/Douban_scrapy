# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider


class Myspider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split('.'))
        # 把Myspider实例self转换为RedisSpider的对象，然后实例化一个类RedisSpider对象
        super(Myspider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url
        }

# -*- coding: utf-8 -*-
import scrapy
from ..items import ZhaopingItem
import redis
from scrapy_redis.spiders import RedisCrawlSpider


class ZhilianSpider(RedisCrawlSpider):
    name = 'zhilian'
    redis_key = "zhilian:start_urls"

    allowed_domains = ['zhilian.com']
    start_urls = ['http://zhilian.com/']

    def start_requests(self):
        """智联招聘北京python职位"""
        url = "https://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&kw=python"
        yield scrapy.Request(url, callback=self.parseMainPage)

    def parseMainPage(self, response):
        item = ZhaopingItem()
        # 获取网页中职位的url数据
        urls = response.xpath('//td[@class="zwmc"]/div/a')
        for url in urls:
            url = url.xpath('@href').extract_first()
            yield scrapy.Request(url, meta={'item': item}, callback=self.parseDetails, dont_filter=True)
        pass

    def parseDetails(self, response):
        """公司职位详情页提取"""
        item = response.meta['item']
        item['job_title'] = response.xpath('//div[@class="fixed-inner-box"]/div[1]/h1/text()').extract_first()
        item['job_info'] = response.xpath('//div[@class="tab-inner-cont"]/p[2]/text()').extract_first()
        item['salary'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract_first()
        item['address'] = response.xpath('//div[@class="tab-inner-cont"]/h2/text()').extract_first()
        item['company'] = response.xpath('//p[@class="company-name-t"]/a/text()').extract_first()
        yield item



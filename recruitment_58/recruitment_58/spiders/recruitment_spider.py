# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from ..items import Recruitment58Item


class PhoneSpiderSpider(RedisSpider):
    name = 'recruitment_spider'
    redis_key = "industry:start_urls"

    custom_settings = {
        'REDIS_START_URLS_AS_SET': True,
    }

    def parse(self, response):
        self.logger("Starting Crawl %s" % response.url)
        resp = response.xpath('//*[@id="list_con"]/li')
        for i in resp:
            item = Recruitment58Item()
            title = i.xpath('.//div[@class="job_name clearfix"]/a/span/text()').extract()
            item['title'] = title[0] + '|' + title[-1]
            item['salary'] = i.xpath('.//p/text()').extract_first()
            item['company'] = i.xpath('./div[@class="item_con job_comp"]/div/a/text()').extract_first()
            item['website'] = i.xpath('.//div[@class="comp_name"]/a/@href').extract_first()
            yield item
        next_page = response.xpath('//div[@class="pagesout"]/a[@class="next"]/@href').extract_first()
        if next_page is not None:
            self.logger.info("Start Crawl: %s" % next_page)
            yield response.follow(next_page, callback=self.parse)
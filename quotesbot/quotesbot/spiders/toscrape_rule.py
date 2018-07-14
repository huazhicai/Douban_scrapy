# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ToscrapeRuleSpider(CrawlSpider):
    name = 'toscrape-rule'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'FEED_FORMAT': 'Json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_URI': 'rule2.json'
    }
    # 必须是列表
    rules = [
        # follow=False(不跟进), 只提取首页符合规则的url，然后爬取这些url页面数据，
        # Follow=True(跟进链接), 在次级url页面中继续寻找符合规则的url,如此循环，直到把全站爬取完毕
        Rule(LinkExtractor(allow=(r'/page/'), deny=(r'/tag/')), callback='parse_item')
    ]

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a/text()').extract()
            }


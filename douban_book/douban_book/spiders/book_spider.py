# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanBookCategoryItem


class BookSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']

    def parse(self, response):
        for resp in response.xpath('//div[@class=article]/div[2]/div'):
            item = DoubanBookCategoryItem()
            item['category'] = resp.xpath('./a/h2/text()').extract_first().replace('.', '').strip()
            for td in resp.xpath('.//td'):
                item['tag'] = td.xpath('./a/text()').extract_first()
                url = td.xpath('./a/@href').extract_first()
                item['url'] = response.urljoin(url)
                item['num'] = td.xpath('./b/text()').extract_first().strip(('(', ')'))
                yield item
                yield scrapy.Request(url, callback=self.parse_tag, meta={'tag': tag}, dont_filter=True)


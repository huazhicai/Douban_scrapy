# -*- coding: utf-8 -*-
import scrapy
from ..items import Top250MusicItem


class MusicsSpider(scrapy.Spider):
    name = 'musics'
    allowed_domains = ['music.douban.com']
    start_urls = ['https://music.douban.com/top250/']
    # 自定义
    custom_settings = {
        'ITEM_PIPELINES': {'top250.pipelines.Top250MusicPipeline': 500}
    }

    def parse(self, response):
        self.logger.info('A response from %s just arrived!' % response.url)
        for element in response.xpath('//tr[@class="item"]'):
            item = Top250MusicItem()
            # 海报
            item['poster'] = element.xpath('.//a[@class="nbg"]/img/@src').extract_first()
            # 标题
            item['title'] = element.xpath('.//div[@class="pl2"]/a/text()').extract_first().replace('\n', '').strip()
            # 链接
            item['link'] = element.xpath('.//div[@class="pl2"]/a/@href').extract_first()

            info = element.xpath('.//div[@class="pl2"]/p[@class="pl"]/text()').extract_first().split('/')
            # 作者
            item['author'] = info[0].strip()
            # 时间
            item['time'] = ((info[1].strip()) if (len(info) > 1) else '')
            # 评分
            item['star'] = element.xpath(
                './/div[@class="pl2"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract_first()
            yield item

        # 加载下一页
        next_page = response.xpath('//div[@class="indent"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

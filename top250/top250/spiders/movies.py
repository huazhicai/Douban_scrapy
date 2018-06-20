# -*- coding: utf-8 -*-
import scrapy
from ..items import Top250MovieItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    # allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250/']

    # 自定义
    custom_settings = {
        'ITEM_PIPELINES': {'top250.pipelines.Top250MoviePipeline': 500}
    }

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        origin_uri = 'https://movie.douban.com/top250'
        for movie in response.xpath('//*[@id="content"]/div/div[1]/ol/li'):
            item = Top250MovieItem()
            item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract_first()
            item['poster'] = movie.xpath('.//div[@class="pic"]/a/img/@src').extract_first()
            movie_titles = movie.xpath('.//div[@class="info"]/div[@class="hd"]/a/span/text()').extract()
            item['title'] = movie_titles[0]
            # 电影别名
            item['alias'] = (movie_titles[1].replace("/", "") if len(movie_titles) > 1 else '')
            # 电影链接
            item['link'] = movie.xpath('.//div[@class="info"]/div[@class="hd"]/a/@href').extract_first()
            # 评分
            item['star'] = movie.xpath(
                './/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            # 影片信息
            item['info'] = movie.xpath('.//div[@class="info"]/div[@class="bd"]/p/text()').extract_first().replace('\n',
                                                                                                                  '').strip()
            # 描述
            item['describe'] = movie.xpath(
                './/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').extract_first()
            yield item
        # 加载下一页 //*[@id="content"]/div/div[1]/div[2]/span[3]/a
        next_page = response.xpath('//div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            # next_page_url = response.urljoin(next_page)
            # yield scrapy.Request(url=next_page_url, callback=self.parse)

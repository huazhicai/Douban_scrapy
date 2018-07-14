# -*- coding: utf-8 -*-
import scrapy
from ..items import AqiItem


class AqispiderSpider(scrapy.Spider):
    name = 'aqispider'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']

    def parse(self, response):
        """
        解析响应，提取所有城市链接，并发送请求，由parse_month解析
        """
        city_link_list = response.xpath('//div[@class="all"]//a/@href').extract()
        city_name_list = response.xpath('//div[@class="all"]//a/text()').extract()

        for link, name in zip(city_link_list, city_name_list)[0:100]:
            url = response.urljoin(link)
            yield scrapy.Request(url, meta={'city': name}, callback=self.parse_month)

    def parse_month(self, response):
        """
        解析每个城市响应，提取所有月份的链接，并发送请求，由parse_day解析
        """
        month_link_list = response.xpath("//tbody//a/@href").extract()
        print("--"*30)
        print(len(month_link_list))     # 43
        for link in month_link_list:
            url = response.urljoin(link)
            yield scrapy.Request(url, meta=response.meta, callback=self.parse_day)

    def parse_day(self, response):
        print(len(response.body))
        city_name = response.meta['city']
        node_list = response.xpath("//tbody/tr[position()>1")    # 30
        node_list.pop(0)
        for node in node_list:
            item = AqiItem()
            item['city'] = city_name
            item['date'] = node.xpath("./td[1]/text()").extract_first()
            item['aqi'] = node.xpath("./td[2]/text()").extract_first()
            item['level'] = node.xpath("./td[3]/span/text()").extract_first()
            item['pm2_5'] = node.xpath("./td[4]/text()").extract_first()
            item['pm10'] = node.xpath("./td[5]/text()").extract_first()
            item['so2'] = node.xpath("./td[6]/text()").extract_first()
            item['co'] = node.xpath("./td[7]/text()").extract_first()
            item['no2'] = node.xpath("./td[8]/text()").extract_first()
            item['o3'] = node.xpath("./td[9]/text()").extract_first()
            print(item["city"])

            yield item




# -*- coding: utf-8 -*-
import scrapy


class ToscrapeSpider(scrapy.Spider):
    name = 'toscrape'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=()))

    )

    def parse(self, response):
        pass

import scrapy
from ..items import QuotesbotItem


class QuotesSpider(scrapy.Spider):
    name = 'toscrape-xpath'
    allowed_domains = ['toscrape.com']
    custom_settings = {
        # 文件存储编码格式
        'FEED_EXPORT_ENCODING': 'utf-8',
        # 文件输出格式
        'FEED_FORMAT': 'csv',
        # 输出文件名，默认路径项目根目录下
        'FEED_URI': 'quote.csv',
        # 设置输出哪些字段，及字段顺序
        'FEED_EXPORT_FIELDS': ["text", "author"]
    }
    # start_urls = ['http://quotes.toscrape.com/tag/%s/' % category,]

    # 因为要对start_urls加工，所以覆盖父类__init__, 但是又继承父类的__init__，
    def __init__(self, category=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://quotes.toscrape.com/tag/%s/' % category,]

    # 起始解析页面必须重写，因为Spider里没用解析功能
    def parse(self, response):
        quote_block = response.xpath('//div[@class="quote"]')
        for quote in quote_block:
            text = quote.xpath('./span[@class="text"]/text()').extract_first()
            author = quote.css('span>small.author::text').extract_first()
            # item = dict(text=text, author=author)
            item = QuotesbotItem()
            item['text'] = text
            item['author'] = author
            yield item

        next_page = response.xpath('//li[@class="next"]/a/href').extract_first()
        if next_page is not None:
            # yield scrapy.Request(response.urljoin(next_page))
            yield response.follow(next_page)
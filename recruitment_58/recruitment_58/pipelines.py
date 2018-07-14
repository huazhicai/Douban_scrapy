# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class RedisDistrictUrlsPipeline(object):
    """
    按行业提取电话销售url存到redis中
    """
    def __init__(self, host, port, db):
        self.redis_client = redis.StrictRedis(
            host=host, port=port, db=db
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("REDIS_HOST"),
            port=crawler.settings.get("REDIS_PORT"),
            db=crawler.settings.get("REDIS_DB"),
        )

    def process_item(self, item, spider):
        redis_key = 'industry:start_urls'
        url = item['url']
        if url:
            self.redis_client.sadd(redis_key, url)
            spider.logger.debug(
                '****** Success push to REDIS with {} ******'.format(url))
            return item


# 对数据库异步操作
class Recruitment58Pipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings.get("MYSQL_HOST"),
            db=settings.get("MYSQL_DB"),
            user=settings.get("MYSQL_USER"),
            passwd=settings.get("MYSQL_PASSWD"),
            charset='utf8',
            use_unicode=True,
        )
        # adbapi.ConnectionPool构造器，进行数据库的异步操作语句
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        # 返回取得的值
        return cls(dbpool)

    # 使用twistd异步插入
    def process_item(self, item, spider):
        query = self.dbpool.runIneraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    # 处理异步插入异常
    def handle_error(self, failure):
        print(failure)

    # 执行具体的插入
    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into recruitment_info(title,salary,company,website) 
                    values (%s,%s,%s,%s)"""
        cursor.execute(insert_sql, (item['title'], item['salary'], item['company'], item['website']))

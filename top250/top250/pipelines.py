# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from . import settings


class Top250MoviePipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
        )
        # 通过cursor执行增删改查
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = "INSERT INTO movies(ranking, poster, title, alias, link, star, info, `describe`)" \
                     " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            self.cursor.execute(insert_sql,
                                (int(item['ranking']), item['poster'], item['title'], item['alias'],
                                 item['link'], item['star'], item['info'], item['describe']))
            self.cursor.connection.commit()
        except BaseException as e:
            print("写入database错误 - ", e)
        return item


class Top250MusicPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
        )
        # 通过游标进行增删改查
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into musics(poster, title, link, author, `time`, star) " \
                     "values(%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(insert_sql, (item['poster'], item['title'], item['link'],
                                             item['author'], item['time'], item['star']))
            self.cursor.connection.commit()
        except BaseException as e:
            print("写入database错误 - ", e)
        return item
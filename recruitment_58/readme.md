## 环境
- win10
- Pycharm
- Python 3.6.1
- Scrapy 1.0
- scrapy_redis
- mysql5.7
## 思路
- 爬取某个城市（以杭州为例）各个行业电销的招聘信息
- 爬虫分为两部分
    - 生产者（industry_spider.py）：爬取各行业电话销售的url， 以集合的方式存储到redis中
    - 消费者（recruitment_spider.py）: 从redis中提取url, 作为初始url。然后爬取详细信息。
- 信息存储到mysql中
## 步骤
- 数据表创建
```
DROP TABLE IF EXISTS `recruitment_info`;

CREATE TABLE `recruitment_info(
`id` int(11) unsigned not null auto_increment,
`title` varvahr(128) not null,
`salary` varchar(64) not null,
`company` varchar(128) not null,
`website` varcahr(128) not null,
primary key `id`,
unique key `url` (`website`)
);
```
- 创建项目：
    - **`scrapy startproject recruitment_58`**
- 构建爬虫：
    - **`scrapy genspider industry_spider hz.58.com/job.shtml`**
    - **`scrapy genspider recruitment_spider hz.58.com/dianhuaxiaoshou`**
import json
import redis
import pymysql


def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(
                    host='127.0.0.1',
                    user='root',
                    passwd='654321',
                    db='test',
                    port=3306,
                    charset='utf8')
    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["sina:items"])
        item = json.loads(data.decode('utf-8'))

        cursor = mysqlcli.cursor()
        # 参数的方式传入
        params = [item['job_title'], item['job_link'], item['job_info'], item['address'], item['company']]
        # 使用execute方法执行SQL INSERT语句
        sql = "INSERT INTO job_items(job_name,job_link,job_info,address,company) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, params)
            cursor.connection.commit()
        except pymysql.Error as e:
            print("插入数据库失败", e)
        cursor.close()
        mysqlcli.close()


if __name__ == '__main__':
    main()

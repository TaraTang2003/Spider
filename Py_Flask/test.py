# -*- coding = utf-8 -*-
# @Time : 2021/11/6 16:14
# @Author : TX
# @File : test.py
# @Software : PyCharm
import pymysql

db = pymysql.connect(host='localhost', user='db', password='123456', database='DoubanTop250')
c = db.cursor()

sql = "SELECT rating_score,count(rating_score) FROM `db250` group by rating_score;"
c.execute(sql)
data = c.fetchall()
print(data)

c.close()
db.close()

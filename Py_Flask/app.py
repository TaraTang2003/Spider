# -*- coding = utf-8 -*-
# @Time : 2021/10/29 17:45
# @Author : TX
# @File : app.py
# @Software : PyCharm

import pymysql
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def home():
    return render_template("index.html")

@app.route('/parts')
def parts():
    return render_template("parts.html")

@app.route('/general')
def general():

    db = pymysql.connect(host='localhost',  user='db',  password='123456', database='DoubanTop250')
    c = db.cursor()

    sql =  "SELECT * FROM db250;"
    c.execute(sql)
    data = c.fetchall()

    c.close()
    db.close()

    return render_template("general.html",movies = data)

@app.route('/analysis')
def analysis():

    datascore = []
    datanum = []

    db = pymysql.connect(host='localhost',  user='db',  password='123456', database='DoubanTop250')
    c = db.cursor()

    sql =  "SELECT rating_score,count(rating_score) FROM `db250` group by rating_score;"
    c.execute(sql)
    data = c.fetchall()
    for item in data:
        datascore.append(item[0])
        datanum.append(item[1])

    c.close()
    db.close()

    return render_template("analysis.html",score = datascore,num =datanum)

@app.route('/test1')
def testECharts():
    return render_template("testECharts.html")

if __name__ == '__main__':
    app.run(port=4000, debug=False)
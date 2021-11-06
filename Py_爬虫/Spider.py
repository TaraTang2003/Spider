# -*- coding = utf-8 -*-
# @Time : 2021/10/26 11:07
# @Author : TX
# @File : Spider.py
# @Software : PyCharm

import requests                  #爬虫伪装，获取源码
from bs4 import BeautifulSoup    #转制存储，选择解析
import re                        #正则表达，筛选数据
import xlwt                      #数据存储
import MySQLdb


def main():
    baseurl = "https://movie.douban.com/top250?start="

    #1.爬取网页
    datalist = getData(baseurl)

    #3.保存数据
    '''savepathEX = "豆瓣电影Top250.xls"
    saveDataEX(datalist, savepathEX)'''

    saveDataDB(datalist)

#正则定义(从html文件中提取信息和并进行分类)
#影片内容链接
findLink = re.compile(r'<a href="(.*?)">') # r表示原生字符串, ‘可以避免与提取内容内“冲突, .任一字符, *前一个字符的0次或多次拓展, ?懒惰模式
#影片图片链接
findImg = re.compile(r'<img.*src="(.*?)".*>', re.S)
#影片名字
findTitle = re.compile(r'<span class="title">(.*?)</span>', re.U) #什么时候贪婪模式，什么时候懒惰模式？
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概述
findInq = re.compile(r'<span class="inq">(.*)</span>', re.S)
#影片其他信息
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

def getData(baseurl):
    """爬取网页，获得数据"""
    datalist  = []
    for page in range(0, 10):
        url = baseurl + str(page * 25)
        html =  askURL(url)

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_ = "item"):
            data = [] #保存一部电影的所有信息
            item = str(item) #正则作用于字符串

            link = re.findall(findLink, item)[0]
            data.append(link)

            img = re.findall(findImg, item)[0]
            data.append(img)

            titles = re.findall(findTitle, item)
            if len(titles) == 2:                              #分别添加中文片名及外文片名
                ctitle = titles[0]
                ftitle = titles[1].replace('\xa0/\xa0', '')
                data.append(ctitle)
                data.append(ftitle)
            else:                                             #无外文片名影片添加中文片名及空字符串
                data.append(titles[0])
                data.append("")

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            judge = re.findall(findJudge, item)[0]
            data.append(judge)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                data.append(inq[0])
            else:
                data.append("")

            bd = re.findall(findBd, item)
            bd = [i.replace('\xa0', '') for i in bd]
            bd = [i.replace('<br/>', '') for i in bd]
            bd = [i.replace('\n', '') for i in bd]
            data.append(bd[0])
            print(data)

            datalist.append(data)

    return datalist

#得到一个指定url的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    try:
        request = requests.get(url, headers=head)
        html = request.content.decode("utf-8")
    except:
        print("爬取失败")
    return html

'''def saveDataEX(datalist, savepathEX):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('豆瓣电影Top250')

    #写入列名
    sheetname = ('影片详情链接', '影片图片链接', '中文片名', '外文片名', '影片评分', '评分人数', '影片概况', '相关信息' )
    for i in range(0, len(sheetname)):
        sheet.write(0, i, sheetname[i])

    #写入项目
    for i in range(1, 251):
        for j in range(0, len(datalist[0])):
            sheet.write(i, j, datalist[i-1][j] )

    book.save(savepathEX)'''

def saveDataDB(datalist):
    __init__DB()
    db = MySQLdb.connect(host = 'localhost', user = 'db', passwd = '123456', db = 'doubantop250', charset = 'utf8')
    c = db.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+str(data[index])+'"'
        print(data)
        sql = '''
            insert into `db250`( `info_link`, `img_link`, `c_name`, `f_name`, `rating_score`, `rating_num`, `intro`, `info`)  
            values(%s) '''%",".join(data)
        c.execute(sql)
        db.commit()

    db.close()

def __init__DB():
    s = '''
        create table if not exists DB250(
        id int primary key AUTO_INCREMENT not null,
        info_link text not null,
        img_link text not null,
        c_name varchar(100) not null,
        f_name varchar(100) not null,
        rating_score double(16,1),
        rating_num numeric,
        intro text not null,
        info text not null
        );
    '''

    db = MySQLdb.connect(host = 'localhost', user = 'db', passwd = '123456', db = 'doubantop250', charset = 'utf8')
    c = db.cursor()
    c.execute(s)
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
    print('爬取成功')
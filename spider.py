#encoding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import openpyxl,mysql.connector
# 获得爬取地址
def getPage(website):
    listnum=[x*25 for x in range(0,10)]
    listurl=[]
    for i in listnum:
        listurl.append("https://movie.douban.com/top250?start="+str(i))
    return listurl
# 获得网页内容并写入数据库
def getList(listurl):
    conn = mysql.connector.connect(user='root', password='password')
    cursor=conn.cursor()
    cursor.execute('create database if not exists movielist;')
    cursor.execute('use movielist;') 
    cursor.execute('create table if not exists movieinfo (Name varchar(20) primary key,Image varchar(255),Url varchar(255),Score varchar(20),Num_person varchar(20));')
    cursor.execute('ALTER TABLE movieinfo DEFAULT CHARACTER SET utf8;')
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 Edg/79.0.309.65"}
    for i in listurl:
        page=requests.get(i,headers=header)
        soup=BeautifulSoup(page.text,"lxml")
        itemlist=soup.select('div.item')
        for j in itemlist:
            name=str(j.select('span.title')[0].string)
            image=str(j.img['src'])
            url=str(j.a['href'])
            score=str(j.select('span.rating_num')[0].string)
            person=str(j.select('span')[-2:][0].string.split('人')[0])
            cursor.execute('insert into movieinfo (Name,Image,Url,Score,Num_person) values (%s,%s,%s,%s,%s)',(name,image,url,score,person))
    conn.commit()
    cursor.close()
    conn.close()
# 主函数
def main():
    wname="douban"
    listurl=getPage(wname)
    getList(listurl)
if __name__=="__main__":
    main()
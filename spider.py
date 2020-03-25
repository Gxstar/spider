#encoding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import openpyxl,mysql.connector
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 Edg/79.0.309.65"}
# 获得爬取地址
#测试一下这台电脑得github
def getPage(website):
    listnum=[x*25 for x in range(0,10)]
    listurl=[]
    for i in listnum:
        listurl.append("https://movie.douban.com/top250?start="+str(i))
    print("爬取网址列表获取成功！")
    return listurl
# 获得网页内容并写入数据库
def getList(listurl):
    conn = mysql.connector.connect(user='root', password='password')
    cursor=conn.cursor()
    cursor.execute('create database if not exists movielist;')
    cursor.execute('use movielist;') 
    cursor.execute('create table if not exists movieinfo (Name varchar(20) primary key,Image varchar(255),Url varchar(255),Score double,Num_person int,Rating_dou int);')
    print("数据库创建成功！")
    global header
    listnum=0
    for i in listurl:
        page=requests.get(i,headers=header)
        soup=BeautifulSoup(page.text,"lxml")
        itemlist=soup.select('div.item')
        for j in itemlist:
            name=str(j.select('span.title')[0].string)
            rating=int(j.select('em')[0].string)
            image=str(j.img['src'])
            url=str(j.a['href'])
            score=float(j.select('span.rating_num')[0].string)
            person=int(j.select('div.bd span')[3].string.split('人')[0])
            listnum+=1
            cursor.execute('insert ignore into movieinfo (Name,Image,Url,Score,Num_person,Rating_dou) values (%s,%s,%s,%s,%s,%s)',(name,image,url,score,person,rating))
            print('\r写入第{0}条成功！'.format(listnum),end='')
    conn.commit()
    cursor.close()
    conn.close()
def searchMovie(movieName):
    i=input("请输入操作指令：")
    global header
    if i=='1':
        url="https://www.dy2018.com"
        page=requests.get(url,headers=header)
        soup=BeautifulSoup(page.text,"lxml")
# 主函数
def main():
    url=getPage('hh')
    getList(url)
if __name__=="__main__":
    main()
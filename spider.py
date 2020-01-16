#encoding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import openpyxl
# 获得爬取地址
def getPage(website):
    listnum=[x*25 for x in range(0,10)]
    listurl=[]
    for i in listnum:
        listurl.append("https://movie.douban.com/top250?start="+str(i))
    return listurl
# 获得网页内容并写入数据库
def getList(listurl):
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 Edg/79.0.309.65"}
    for i in listurl:
        page=requests.get(i,headers=header)
        soup=BeautifulSoup(page.text,"lxml")
# 主函数
def main():
    wname="douban"
    listurl=getPage(wname)
    getList(listurl)
if __name__=="__main__":
    main()
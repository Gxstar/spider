#encoding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import openpyxl
class article(object):
    def __init__(self):
        self.title=""
        self.date=""
        self.cat=""
        self.hot=""
        self.comment=""
        self.intro=""
def getPage(url):
    data=requests.get(url)
    return data.text
def getList(body):
    articleList=[] 
    for i in body.find_all(class_='post-content'):
        temp=article()
        temp.title=i.select("div>a.post-title")[0].text.replace("\n","").replace("\t","")
        temp.date=i.select("div>div.post-date")[0].text.replace("\n","").replace("\t","")
        temp.hot=i.select("div>div.post-meta span")[0].text.replace("\n","").replace("\t","")
        temp.comment=i.select("div>div.post-meta span")[1].text.replace("\n","").replace("\t","")
        temp.cat=i.select("div>div.post-meta span")[2].text.replace("\n","").replace("\t","")
        temp.intro=i.select("div>div.float-content")[0].text.replace("\n","").replace("\t","")
        articleList.append(temp)
    return articleList
def main():
    url="https://gxstar123.cn"
    page=getPage(url)
    soup=BeautifulSoup(page,"lxml")
    articleList=getList(soup)
    print(articleList)
    wb=openpyxl.Workbook()
    ws=wb.create_sheet(index=0,title="结果")
    ws.append(['标题','日期','分类','热度','评论','摘要'])
    for i in articleList:
        ws.append([i.title,i.date,i.cat,i.hot,i.comment,i.intro])
    wb.save('result.xlsx')
    wb.close()
if __name__=="__main__":
    main()
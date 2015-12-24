# -*- coding:utf-8 -*-
import sys,os
import time
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
import threading

#g_url=[]    #要爬取的url连接列表
#g_imgurl=[]     #要爬去的img连接表
class spiderUrl:
    def __init__(self,url):
        self.url = url
        self.header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36","Host":"www.mzitu.com"}
        self.g_url= {}
        self.g_imgurl = []
        self.flage = ""
        self.name = ""
##保存为本地文件
    def saveImg(self,imgurl,filename):
        data = urllib2.urlopen(imgurl).read()
        f = open(filename,'wb')
        f.write(data)
        print "正在悄悄保存一张照片为:", filename
        f.close()

    def saveInDir(self,name,imgurl):
        number = 1
        name = name.encode("gbk")
        print "共发现",len(imgurl),"张照片"
        for url in imgurl:
            filename = "%s/%s(%d).jpg" % (name,name,number)
            if os.path.isfile(filename):
                print "已经爬过她了~~"
                continue
            self.saveImg(url,filename)
            number += 1




##文件夹创建
    def MakeDir(self,path):
       path = path.strip()
       #判断路径下的文件夹是否存在
       isExists = os.path.exists(path)
       if not isExists:
           print "悄悄创建了"+path+"文件夹"
           os.makedirs(path)
           return True
       else:
           print path+"文件夹已经创建成功了"
           return False


#获取网页的源码
    def getPageCode(self,url):
        try:
            request = urllib2.Request(url,headers=self.header)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode("utf-8")
            return pageCode
        except urllib2.HTTPError , e:
            if hasattr(e,"code"):
                print e.code
                return None
            if hasattr(e,"reason"):
                print e.reason
                return None

#获取要爬的页面    会在全局变量中保存要收集相片的主页地址.
    def getPageUrl(self,pagecode):
        g_url = {}
        soup = BeautifulSoup(pagecode)
        target = soup.body.find("div",class_="postlist").ul.find_all("a",text=re.compile(r'\W+'))
        for url in target:
            g_url[url.text] = url.get('href')
        return g_url

#获取要爬的照片的URL
    def getImgUrl(self,pageurl,flage):
        pagecode = self.getPageCode(pageurl)
        soup = BeautifulSoup(pagecode)
        nexturl = soup.body.find("div",class_='main-image').p.a.get('href')
        targetImg = soup.body.find("div",class_='main-image').p.img.get('src')
        self.g_imgurl.append(targetImg)
        if flage not in nexturl:   ## 判断是否已经到了一组图的最后一张
            return
        self.getImgUrl(nexturl,flage)

#开始下载妹子的图片
    def getImg(self):
        pagecode = self.getPageCode(self.url)
        g_url = self.getPageUrl(pagecode)
        for name,url in g_url.items():
            self.g_imgurl = []
            self.MakeDir(name.encode("gbk"))
            self.getImgUrl(url,url.split("/")[-1])
            self.saveInDir(name,self.g_imgurl)

    def printUrl(self):
        print self.g_imgurl







if __name__ == "__main__":
    url = "http://www.mzitu.com/xinggan"
    spider = spiderUrl(url)
    spider.getImg()
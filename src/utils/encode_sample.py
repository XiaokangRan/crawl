#!/usr/bin/env python
#coding=utf-8
import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import chardet
url = 'https://baike.baidu.com/item/%E8%94%A1%E5%BE%90%E5%9D%A4'
headers_pc = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}

response = requests.get(url,headers=headers_pc,timeout=10)
response.content.decode('utf-8')
soup = BeautifulSoup((response), 'lxml')
line=Selector(text=response.content.decode('utf-8'))
line=Selector(text=response.text).xpath('//div[contains(@class, "main-content")]')
title=line.xpath('//h1//text()').extract()

line=Selector(text=response.content.decode('utf-8')).xpath('//div[contains(@class, "main-content")]')
title=line.xpath('//h1//text()').extract()


#编码不对
select=Selector(text=response.text).xpath('//div[contains(@class, "main-content")]').xpath('//h1//text()').extract()
#编码正确
Selector(text=response.content.decode('utf-8')).xpath('//div[contains(@class, "main-content")]').xpath('//h1//text()').extract()
Selector(text=response.content.decode('utf-8')).xpath('//h1//text()').extract()  #编码正确
Selector(text=response.content.decode('utf-8')).xpath('//div[contains(@class, "main-content")]').xpath('..//..//..//../h1//text()').extract()

##
selector=Selector(text=response.content)
names=selector.xpath('//dt[contains(@class,"basicInfo-item name")]').extract()
values=selector.xpath('//dd[contains(@class,"basicInfo-item value")]').extract()

#response.content      bytes对象
#response.text         str对象
#str与bytes转换关系：encode 和 decode
#encode：str->bytes; decode: bytes->str
#查看某个字符串编码: s = '张三' print(chardet.detect(str.encode(s)))
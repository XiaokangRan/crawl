#
import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        headers_pc = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                   'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}
        # headers_mobile={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36',
        #                 "Accept":"text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8"}
        response = requests.get(url,headers=headers_pc,timeout=10)
        if response.status_code != 200:
            return None
        return response.content

url = 'https://baike.baidu.com/item/%E8%94%A1%E5%BE%90%E5%9D%A4'
download = HtmlDownloader()
contents = download.download(url)
selector=Selector(text=contents)
title = ''.join(selector.xpath('//h1/text()').extract()).replace('/','').replace(',', '，')
names = selector.xpath('//dt[contains(@class,"basicInfo-item name")]').extract()
values = selector.xpath('//dd[contains(@class,"basicInfo-item value")]').extract()
lines=''
for i, name in enumerate(names):
    # name
    temp = Selector(text=name).xpath('//dt/text()|//dt/a/text()').extract()  # 得到key值
    name = ''.join(temp).replace('\n', '').replace(',', '，').replace('\xa0', '').replace(' ', '')
    # value
    temp = Selector(text=values[i]).xpath('//dd/text()|//dd/a/text()').extract()
    value = ''.join(temp).replace('\n', '').replace(',', '，')
    lines += title + ',' + name + ',' + value + '\n'
    print(title + ',' + name + ',' + value + '\n')


import os
import sys
sys.path.insert(0, os.path.join("../../../"))
import time
from lxml import etree
from src.conf import *
from src.log import *
from src.proxy import *
from src.main.parse import *
from src.main.const import *
from bs4 import BeautifulSoup

class HotTv(Spider):
    def __init__(self):
        super().__init__()
        self.url = "https://www.baidu.com/s?wd=%E7%83%AD%E9%97%A8%E7%94%B5%E8%A7%86%E5%89%A7&rsv_spt=1&rsv_iqid=0xc480bdd200025744&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=78040160_14_pg&ch=16&rsv_enter=1&rsv_dl=tb&oq=python%2520xpath&inputT=4624&rsv_t=af679HOsXAR5cv4U7Vr%2Bny9hDyEIEBAYhQzwyGgp6PHan7D5bPPdLuRLFMHP8UDxa7VWxQc&rsv_pq=e4170e340021f8c3&rsv_sug3=29&rsv_sug1=17&rsv_sug7=100&rsv_sug2=0&rsv_sug4=4624"
    def parse_page_info(self, response):
        return response

    def web_test(self,url):
        self.web_browser()

    def crawl_all_info(self):
        all_data = []
        page = 0
        while page < 120:
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            movie_list_1 = soup.find("div",attrs={'id':"content_left"}).find('div', attrs={'class':'c-border'}).find('div', attrs={
                'class':'op_exactqa_main'}).find('div',attrs={"class":'op_exactqa_body'}).find_all('div', attrs={
                'class':"op_exactqa_item c-gap-bottom c-span6 "})

            movie_list_2 = soup.find("div",attrs={'id':"content_left"}).find('div', attrs={'class':'c-border'}).find('div', attrs={
                'class':'op_exactqa_main'}).find('div',attrs={"class":'op_exactqa_body'}).find_all('div', attrs={
                'class': "op_exactqa_item c-gap-bottom c-span6 c-span-last"})

            for movie_soup in movie_list_1:
                movie_info = movie_soup.find_all('p')
                name = movie_info[1].text
                rate = movie_info[2].text
                all_data.append((name, rate))
            for movie_soup in movie_list_2:
                movie_info = movie_soup.find_all('p')
                name = movie_info[1].text
                rate = movie_info[2].text
                all_data.append((name, rate))
            self.browser.find_element_by_xpath("//span[contains(text(),'下一页')]").click()
            page = page + 1
            print("page is: "+str(page))
            time.sleep(2)
        print("len is: "+str(len(all_data)))
        all_data = [",".join(x) for x in all_data]
        with open("tv.txt", 'w', encoding='utf-8') as f:
            f.write("\n".join(all_data))
            f.write("\n")

    def get_content(self):
        soup = BeautifulSoup(spider.browser.page_source, "html.parser")
        star_name_list = soup.find_all("p", attrs={"class": "star-name"})

    def run(self):
        try:
            self.web_browser()
            self.browser.get(self.url)
            self.crawl_all_info()
            self.browser.quit()
        except Exception as err:
            self.browser.quit()
            print(str(err))

if __name__ == '__main__':
    tv_spider = HotTv()
    tv_spider.run()

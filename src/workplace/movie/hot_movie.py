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

class HotMovie(Spider):
    def __init__(self):
        super().__init__()
        self.url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=16&tn=78040160_14_pg&wd=%E7%83%AD%E9%97%A8%E7%94%B5%E5%BD%B1&oq=%25E7%2583%25AD%25E9%2597%25A8%25E7%2594%25B5%25E5%25BD%25B1&rsv_pq=9c1af4720008fd6e&rsv_t=46fdOW76Crwxc6JUWei9IILr%2FR11%2F1X7YujH3DemNunbo%2FOjogMOwHUs011U5Md1pkR4m7A&rqlang=cn&rsv_enter=0&rsv_dl=tb"

    def parse_page_info(self, response):
        return response

    def web_test(self,url):
        self.web_browser()

    def crawl_all_info(self):
        all_data = []
        page = 0
        while page < 121:
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
        print(all_data)
        with open("movie.txt", 'w', encoding='utf-8') as f:
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
    movie_spider = HotMovie()
    movie_spider.run()

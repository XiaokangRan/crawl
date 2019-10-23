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

class HotActor(Spider):
    def __init__(self):
        super().__init__()
        self.url = "https://baike.baidu.com/starrank"

    def parse_page_info(self, response):
        return response

    def web_test(self,url):
        self.web_browser()

    def crawl_all_info(self):
        all_data = []
        page = 0
        while page < 100:
            star_name_list = self.browser.find_elements_by_class_name("star-name")
            print(star_name_list[-1].text)
            actor_names = [actor.text for actor in star_name_list]
            all_data.extend(actor_names)
            self.browser.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
            page = page + 1
            print("page is: "+str(page))
            time.sleep(1.3)
        print("len is: "+str(all_data))
        with open("actor.txt", 'w', encoding='utf-8') as f:
            f.write("\n".join(all_data))
            f.write("\n")

    def get_content(self):
        soup = BeautifulSoup(spider.driver.page_source, "html.parser")
        star_name_list = soup.find_all("p", attrs={"class": "star-name"})

    def run(self):
        try:
            self.web_browser()
            self.browser.get(self.url)
            self.crawl_all_info()
            self.browser.close()
        except Exception as err:
            self.browser.close()
            print(str(err))

if __name__ == '__main__':
    actor_spider = HotActor()
    actor_spider.run()


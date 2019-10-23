import os
import sys
sys.path.insert(0, os.path.join("../../../"))

from lxml import etree
from src.conf import *
from src.log import *
from src.proxy import *
from src.main.parse import *
from src.main.const import *


class HotActor(Spider):
    def __init__(self):
        super().__init__()
        self.url = "https://baike.baidu.com/starrank"

    def parse_page_info(self, response):
        return response


if __name__ == '__main__':
    actor_spider = HotActor()
    soup = actor_spider.get_xpath_soup(actor_spider.url)
    result = soup.xpath("/html/body/div[1]/div/div[4]/div[1]/table/tbody/tr[1]/td[2]/a/div[2]/p[1]"+"/text()")
    print(result)
    actor_spider.parse_page_info(result)

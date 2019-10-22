import os
import sys
sys.path.insert(0, os.path.join("../../../"))

from src.conf import *
from src.log import *
from src.proxy import *
from src.main.parse import *
from src.main.const import *


class HotActor(Spider):
    def __init__(self):
        super(HotActor, self).__init__()
        self.url = "https://baike.baidu.com/starrank"

    def parse_page_info(self, response):
        return response

if __name__ == '__main__':
    spider = HotActor()
    response = spider.get_html(spider.url)
    HotActor.parse_page_info(response)

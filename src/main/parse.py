import logging
import logging.config
import yaml
import sys
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import json
import redis
import pymongo
import time

from multiprocessing.dummy import Pool as ThreadPool
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

proxy = {'https': '36.71.150.87:80'}

class Spider:

    def __init__(self):
        self.config()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.proxies = None
    def time_cal(self):
        now = time.time()
        print(time.time() - now)
        return

    def config(self):
        # 初始化log
        abs_path = os.path.abspath(sys.argv[0])
        try:
            log_config_file_path = 'F:\\Git Program\\crawl\\src\\log\\log_config.yaml'
            with open(log_config_file_path, 'r', encoding='utf-8') as f:
                #log_config = yaml.load(f)
                log_config = yaml.safe_load(f.read())
            logging.config.dictConfig(log_config)
            self.spider_log = logging.getLogger('spider')
            self.spider_log.info('Logger初始化成功')
        except Exception as err:
            print('Logger初始化失败' + str(err))

        # 初始化配置
        try:
            spider_cofig_file_path = 'F:\\Git Program\\crawl\\src\\conf\\spider_config.yaml'
            with open(spider_cofig_file_path, 'r', encoding='utf-8') as f:
                spider_config = yaml.safe_load(f.read())
                self.config = spider_config
                self.spider_log.info('Config初始化成功')
        except Exception as err:
            self.spider_log.error('Config初始化失败' + str(err))

        # 初始化redis
        try:
            redis_host = self.config['redis']['host']
            redis_port = self.config['redis']['port']
            self.redis_con = redis.Redis(host=redis_host, port=redis_port, db=0)
            # 刷新redis库
            self.redis_con.flushdb()
            self.spider_log.info('Redis初始化成功')
        except Exception as err:
            self.spider_log.error('Redis初始化失败' + str(err))

        # Mongo
        """
        try:
            myclient = pymongo.MongoClient('localhost', 27017)
            dblist = myclient.list_database_names()
            mydb = myclient['db']
            self.mytable = mydb['info']
        except Exception as err:
            self.spider_log.info('mongodb初始化失败' + str(err))
        """

    def web_browser(self):
        # browser
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        self.browser = webdriver.Chrome(options=opt)
        #self.browser.quit()

    def browser_test(self, url="https://baike.baidu.com/starrank"):
        self.web_browser()
        self.browser.get(url)
        print(self.browser.page_source)
        score_num_element = self.browser.find_elements_by_class_name("star-name")
        return score_num_element

    def proxy(self):
        return

    def _is_parse_movie_id(self, name):
        try:
            if self.redis_con.hexists('already_parse_movie', name):
                # self.movie_spider_log.info('已经解析过' + str(name) + '电影')
                return True
            else:
                self.redis_con.hset('already_parse_movie', name, 1)
                # self.movie_spider_log.info('没有解析过' + str(name) + '电影, 等待解析')
                return False
        except Exception as err:
            return False

    def get_html(self, url):
        r = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=3)
        if r.status_code == 200:
            return r.text
        else:
            return None

    def get_xpath_soup(self, url):
        """
        use：result = soup.xpath("/html/body/div[1]/div/div[4]/div[1]/table/tbody/tr[1]/td[2]/a/div[2]/p[1]")[0].text
            or: result = soup.xpath("/html/body/div[1]/div/div[4]/div[1]/table/tbody/tr[1]/td[2]/a/div[2]/p[1]/text()")
        :param url: "https://baike.baidu.com/starrank"
        :return: soup
        """
        response = self.get_html(url)
        if response is not None:
            soup = etree.HTML(response)
            return soup
        else:
            return None

    def get_soup(self, url):
        response = self.get_html(url)
        if response is not None:
            soup = BeautifulSoup(response, 'html5lib')
            return soup
        else:
            return None
        return soup

    def parse_page_info(response):
        return

    def get_all_info(self):
        return

    def craw_all_info(self):
        return

    def parse_page_info(self, url):
        return

    def run(self):
        return


if __name__ == '__main__':
    spider = Spider()
    spider.run()
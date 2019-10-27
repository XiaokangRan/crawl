import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import pickle
import threading
import url_manager
import time
import sys
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
from multiprocessing import Manager


class HtmlDownloader(object):
    @staticmethod
    def download(url):
        if url is None:
            return None
        headers_pc = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                   'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}
        response = requests.get(url, headers=headers_pc, timeout=10)
        if response.status_code != 200:
            return None
        return response.content

#url = 'https://baike.baidu.com/item/%E8%94%A1%E5%BE%90%E5%9D%A4'   #actor
# url = 'https://baike.baidu.com/item/%E6%88%98%E7%8B%BC%E2%85%A1?fromtitle=%E6%88%98%E7%8B%BC2&fromid=17196087#3' #movie
url = 'https://baike.baidu.com/item/天下第一'

class HtmlParse(object):
    @staticmethod
    def parse(contents):
        try:
            selector = Selector(text=contents)
            title = ''.join(selector.xpath('//h1/text()').extract()).replace('/','').replace(',', '，')
            names = selector.xpath('//dt[contains(@class,"basicInfo-item name")]').extract()
            values = selector.xpath('//dd[contains(@class,"basicInfo-item value")]').extract()
            movie_data = []
            role_data = []
            for i, name in enumerate(names):
                # name
                temp = Selector(text=name).xpath('//dt/text()|//dt/a/text()').extract()  # 得到key值
                name = ''.join(temp).replace('\n', '').replace(',', '，').replace('\xa0', '').replace(' ', '')
                # value
                temp = Selector(text=values[i]).xpath('//dd/text()|//dd/a/text()').extract()
                value = ''.join(temp).replace('\n', ';').replace(',', '，').replace('\xa0', '')
                movie_data.append((title, name, value))

            roles = selector.xpath('//dl[contains(@class, "roleIntrodcution-descritpion")]').extract()
            for i, role in enumerate(roles):
                soup = BeautifulSoup(role, 'html5lib')
                # role_name
                role_name = soup.find(name='div', class_="role-name").find(name='span',class_="item-value").text
                role_name = role_name.replace("\n", '').replace('\xa0', '').replace(',', '，')
                # role_actor
                role_actor = soup.find(name='div', class_="role-actor").find(name='span',class_="item-value").text
                role_actor = role_actor.replace("\n", '').replace('\xa0', '').replace(',', '，')
                #role_intor
                role_intor = soup.find(name='dd', class_="role-description").text
                role_intor = role_intor.replace("\n", '').replace('\xa0', '').replace(',', '，')

                movie_data.append((title, role_name, role_actor))
                role_data.append((title, role_name, role_actor, role_intor))
            return movie_data, role_data
        except Exception as err:
            print("htmlParse occur err")
            return None, None

def run(url):
    try:
        url = 'https://baike.baidu.com/item/' + url
        print(url)
        download = HtmlDownloader()
        parse = HtmlParse()
        contents = download.download(url)
        movie_data, role_data = parse.parse(contents)
        lock.acquire()
        if movie_data is not None:
            if len(movie_data) != 0:
                movie_save.append(movie_data)
        if role_data is not None:
            if len(role_data) != 0:
                role_intro_save.append(role_data)
        lock.release()
        time.sleep(1)
    except Exception as err:
        print(err)

def init(l, m, r):
    global lock
    global movie_save
    global role_intro_save
    lock = l
    movie_save = m
    role_intro_save = r

if __name__ == '__main__':
    #ulrs = set()
    urls = url_manager.UrlManager()
    # 读取电影名
    with open('movie_test.txt', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    movie_name = []
    for line in lines:
        urls.add_new_url(line)
        movie_name.append(line)
    save_path = './save'
    movie_save = []
    role_intro_save = []
    count_thread = 12
    lock = multiprocessing.Lock()
    pool = multiprocessing.Pool(processes=count_thread, initializer=init, initargs=(lock, movie_save, role_intro_save))
    pool.map(run, movie_name)
    pool.close()
    pool.join()
    print(".........saving.........")
    pickle.dump(movie_save, open(save_path, 'wb'))
    pickle.dump(role_intro_save, open('./save_role', 'wb'))
    print(".........saved.........")
    print (movie_save)


manager = multiprocessing.Manager()
movie_list = manager.list()
role_list = manager.list()











"""
    LOCK = threading.Lock()
    threads=[]
    count_thread=12
    for i in range(count_thread):
        print(f'build thread {i+1}...')
        threads.append(movie())
    try:
        for t in threads:
            t.start()
            t.join()
    except:
        print('thread error!')
        print("saving.........")
        pickle.dump(movie_save, open(save_path, 'wb'))
        pickle.dump(role_intro_save, open('./save_role', 'wb'))
        print("saved.........")
        sys.exit(1)
    finally:
        print("saving.........")
        pickle.dump(movie_save, open(save_path, 'wb'))
        pickle.dump(role_intro_save, open('./save_role', 'wb'))
        print("saved.........")
"""
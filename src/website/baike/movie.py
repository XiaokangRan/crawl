import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import pickle
import threading
import url_manager
import time
import sys

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
            #lines=''
            data = []
            for i, name in enumerate(names):
                # name
                temp = Selector(text=name).xpath('//dt/text()|//dt/a/text()').extract()  # 得到key值
                name = ''.join(temp).replace('\n', '').replace(',', '，').replace('\xa0', '').replace(' ', '')
                # value
                temp = Selector(text=values[i]).xpath('//dd/text()|//dd/a/text()').extract()
                value = ''.join(temp).replace('\n', '').replace(',', '，')
                data.append((title, name, value))
                #print(title + ',' + name + ',' + value + '\n')

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
                #print(role_name, role_actor)
                #print(role_intor)
                data.append((title, name, value))
            return data
        except Exception as err:
            print("htmlParse occur err")
            return None



def movie():
    LOCK.acquire()
    try:
        url = urls.get_new_url()
    except Exception as err:
        print(err)
        print('save state', sys.exc_info())
        print(".........saving.........")
        pickle.dump(movie_save, open(save_path, 'wb'))
        print(".........saved.........")
        sys.exit(1)
    url = 'https://baike.baidu.com/item/' + url
    LOCK.release()
    download = HtmlDownloader()
    parse = HtmlParse()
    contents = download.download(url)
    data = parse.parse(contents)
    LOCK.acquire()
    if data is not None:
        movie_save.append(data)
    LOCK.release()
    time.sleep(1)
    print(data[0])
    return data

if __name__ == '__main__':
    #ulrs = set()
    urls = url_manager.UrlManager()
    # 读取电影名
    with open('movie.txt', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        urls.add_new_url(line)
    save_path = './save'
    movie_save = []
    count_thread = 12
    #movie_data = pickle.load(open(save_path, 'rb'))
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
        for t in threads:
            t.terminate()
        print('error!', sys.exc_info()[0])
        print("saving.........")
        pickle.dump(movie_save, open(save_path, 'wb'))
        print("saved.........")
    finally:
        print('finished,saving state')
        pickle.dump(movie_save, open(save_path, 'wb'))

import requests
from bs4 import BeautifulSoup
import json

class CrawlIp(object):
    def __init__(self):
        """初始化变量"""
        self.url = [
            "https://www.xicidaili.com/nn/1",
            'https://www.xicidaili.com/nn/2',
            "https://www.xicidaili.com/nn/3"
        ]
        self.check_url = 'https://www.ip.cn/'
        self.ip_list = []

    @staticmethod
    def get_html(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        try:
            request = requests.get(url=url, headers=headers)
            request.encoding = 'utf-8'
            html = request.text
            return html
        except Exception as e:
            return ''

    def get_available_ip(self, ip_address, ip_port):
        """检测IP地址是否可用"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        ip_url_next = '://' + ip_address + ':' + ip_port
        proxies = {'http': 'http' + ip_url_next, 'https': 'https' + ip_url_next}
        try:
            r = requests.get(self.check_url, headers=headers, proxies=proxies, timeout=3)
            html = r.text
        except:
            print('fail-%s' % ip_address)
        else:
            print('success-%s' % ip_address)
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find(class_='well')
            if div:
                print(div.text)
            # ip_info = {'address': ip_address, 'port': ip_port}
            ip_info = 'https://' + ip_address + ":" + ip_port
            self.ip_list.append(ip_info)
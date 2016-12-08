from utils import get_page, Downloader
from bs4 import BeautifulSoup
import time

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class CrawlFreeProxy(object, metaclass=ProxyMetaclass):

    def __init__(self):
        pass
    
    def get_raw_proxies(self, callback, count=40):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
            if len(proxies) >= count:
                break
        return proxies

    def crawl_kuaidaili(self, page_count=8):
        start_url = 'http://www.kuaidaili.com/proxylist/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            soup = get_page(url) 
      
            proxy_list = soup.find('div', {'id': 'index_free_list'}).find('tbody')
            for proxy in proxy_list.find_all('tr'):
                ip = proxy.find_all('td')[0].get_text()
                port = proxy.find_all('td')[1].get_text()
                yield ':'.join([ip, port])


    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            soup = get_page(url) 
            time.sleep(1)
            proxy_list = soup.find('table', {"border": "2px"}) 
            for proxy in proxy_list.find_all('tr')[1:]:
                ip = proxy.find_all('td')[0].get_text()
                port = proxy.find_all('td')[1].get_text()
                yield ':'.join([ip, port])

    def crawl_xici(self):
        start_url = 'http://api.xicidaili.com/free2016.txt'
        soup = get_page(start_url)
        proxy_list = soup.find('p') 
        return proxy_list.get_text().split('\r\n')
    
    def crawl_proxy360(self):
        start_url = 'http://www.proxy360.cn/default.aspx'
        soup = get_page(start_url)
        for proxy in soup.find_all('div', {"class": "proxylistitem"}):
            item = proxy.find_all('span', {"class": "tbBottomLine"})
            ip = item[0].get_text().replace('\r\n', '').replace(' ', '')
            port = item[1].get_text().replace('\r\n', '').replace(' ', '')
            yield ':'.join([ip, port])
    
    # def crawl_goubanjia(self):
    #     start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
    #     soup = get_page(start_url)
    #     proxy_list = soup.find('table', {"class": "table"}).find('tbody')
    #     for tr in proxy_list.find_all('tr'):
    #         _proxy = tr.find('td').find_all('span')
    #         proxy = [i.get_text() for i in _proxy]
    #         yield ''.join(proxy)


if __name__ == '__main__':
    import time
    a = CrawlFreeProxy()
    start = time.clock()
    print(list(a.crawl_goubanjia()))

    
    print(time.clock()-start)
    
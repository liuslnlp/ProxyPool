from utils import get_page, Downloader
from bs4 import BeautifulSoup

class CrawlFreeProxy(object):

    def __init__(self):
        pass
    
    def get_raw_proxies(self, engine='1', count=40):
        pass

    def crawl_kuaidaili(self, page_count=8):
        start_url = 'http://www.kuaidaili.com/proxylist/{}/'
        urls = [start_url.format(str(page)) for page in range(1, page_count + 1)]
        # d = Downloader(urls)
        # htmls = d.htmls
 
        # for html in htmls:
        #     soup = BeautifulSoup(html, 'lxml')

        #     proxy_list = soup.find('div', {'id': 'index_free_list'}).find('tbody')
        #     for proxy in proxy_list.find_all('tr'):
        #         ip = proxy.find_all('td')[0].get_text()
        #         port = proxy.find_all('td')[1].get_text()
        #         yield ':'.join([ip, port])


        for url in urls:
            soup = get_page(url)
            
            proxy_list = soup.find('div', {'id': 'index_free_list'}).find('tbody')
            for proxy in proxy_list.find_all('tr'):
                ip = proxy.find_all('td')[0].get_text()
                port = proxy.find_all('td')[1].get_text()
                yield ':'.join([ip, port])


    def crawl_daili66(self):
        pass

    def crawl_xici(self):
        pass

if __name__ == '__main__':
    import time
    a = CrawlFreeProxy()
    start = time.clock()
    for i in a.crawl_kuaidaili():
        print(i)
    
    print(time.clock()-start)
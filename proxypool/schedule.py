from threading import Thread
from proxyGetter import CrawlFreeProxy
from vaildityTester import VaildityTester
from db import RedisClient
import time


class Schedule(object):

    def __init__(self):
        self.__conn = RedisClient()
        self.__crawler = CrawlFreeProxy()

    def vaild_proxy(self, cycle=10):
        while True:
            count = int(0.25 * self.__conn.queue_len)
            raw_proxies = self.__conn.get(count)
            # usable_proxies =

    def check_pool(self, threshold=10, cycle=10):
        while True:
            if self.__conn.queue_len < threshold:
                self.add_proxy()
            time.sleep(cycle)
    
    # 从这往下，全部重写

    def add_proxy(self, threshold=30):
        raw_proxies = self.__crawler.get_raw_proxies()
        tester = VaildityTester(raw_proxies)
        tester.test()
        for proxy in tester.get_usable_proxies():
            self.__conn.put(proxy)
        if self.__conn.queue_len < threshold:
            self.add_proxy()
        

    def start_schedule(self):
        vaild_thread = Thread(target=self.vaild_proxy)
        check_thread = Thread(target=self.check_pool)
        vaild_thread.start()
        check_thread.start()

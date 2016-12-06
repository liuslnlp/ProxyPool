from db import RedisClient
from vaildityTester import VaildityTester
from proxyGetter import CrawlFreeProxy


class PoolAdder(object):

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = VaildityTester()
        self._crawler = CrawlFreeProxy()

    def is_over_threshold(self):
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False
    
    def add(self):
        # 增加一些抓取逻辑，防止对同一页面的持续抓取
        raw_proxies = self._conn.get()
        self._tester.set_raw_proxies(raw_proxies)
        self._tester.test()
        self._conn.put_many(self._tester.get_usable_proxies())
        if self.is_over_threshold():
            return 
        self.add()

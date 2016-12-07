from db import RedisClient
from vaildityTester import VaildityTester
from proxyGetter import CrawlFreeProxy
from error import ResourceDepletionError


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

    def add_to_queue(self):
        flag = 40
        while not self.is_over_threshold:
            raw_proxies = self._crawler.get_raw_proxies(flag)
            self._tester.set_raw_proxies(raw_proxies)
            self._tester.test()
            self._conn.put_many(self._tester.get_usable_proxies())
            flag += 40

            if flag >= 400:
                raise ResourceDepletionError

from db import RedisClient
from vaildityTester import VaildityTester
from proxyGetter import FreeProxyGetter
from error import ResourceDepletionError


class PoolAdder(object):
    """
    添加器，负责向池中补充代理
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = VaildityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        判断代理池中的数据量是否达到阈值。
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        """
        命令爬虫抓取一定量未检测的代理，然后检测，将通过检测的代理
        加入到代理池中。
        """

        flag = 40
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback, flag)
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                self._conn.put_many(self._tester.get_usable_proxies())
                if self.is_over_threshold():
                    break

            flag += flag
            if flag >= 10 * flag:
                raise ResourceDepletionError

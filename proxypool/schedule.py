"""
调度器模块
"""
from threading import Thread
from multiprocessing import Process
from db import RedisClient
import time
import asyncio
import aiohttp
from error import ResourceDepletionError
from proxyGetter import FreeProxyGetter


class VaildityTester(object):
    """
    检验器，负责对未知的代理进行异步检测。
    """

    test_api = 'https://www.baidu.com'

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []
        

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._usable_proxies = []

    async def test_single_proxy(self, proxy):
        async with aiohttp.ClientSession() as session:
            try:
                real_proxy = 'http://' + proxy
                async with session.get(self.test_api, proxy=real_proxy, timeout=15) as resp:
                    self._usable_proxies.append(proxy)
            except asyncio.TimeoutError:
                pass

    def test(self):
        loop = asyncio.get_event_loop()
        tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
        loop.run_until_complete(asyncio.wait(tasks))

    def get_usable_proxies(self):
        return self._usable_proxies


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

    def add_to_queue(self, flag=40):
        """
        命令爬虫抓取一定量未检测的代理，然后检测，将通过检测的代理
        加入到代理池中。
        """
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


class Schedule(object):
    
    @staticmethod
    def vaild_proxy(cycle=600):
        conn = RedisClient()
        tester = VaildityTester()
        while True:
            time.sleep(cycle)
            count = int(0.25 * conn.queue_len)
            if count == 0:
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            proxies = tester.get_usable_proxies()
            conn.put_many(proxies)

    @staticmethod
    def check_pool(lower_threshold=10, upper_threshold=30, cycle=20):
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        vaild_thread = Process(target=Schedule.vaild_proxy)
        check_thread = Process(target=Schedule.check_pool)
        vaild_thread.start()
        check_thread.start()
        # vaild_thread.join()
        # check_thread.join()

if __name__ == '__main__':
    schedule = Schedule()
    schedule.run()
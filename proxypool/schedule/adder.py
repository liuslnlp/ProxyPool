from ..conf import POOL_UPPER_THRESHOLD
from ..dbop import RedisOperator
from ..errors import ResourceDepletionError
from ..spiders import SpiderMeta
from .tester import UsabilityTester
from concurrent import futures


class PoolAdder(object):
    """添加器，负责启动爬虫补充代理"""

    def __init__(self):
        self._threshold = POOL_UPPER_THRESHOLD
        self._pool = RedisOperator()
        self._tester = UsabilityTester()

    def is_over(self):
        """ 判断池中代理的数量是否达到阈值
        :return: 达到阈值返回 True, 否则返回 False.
        """
        return True if self._pool.size >= self._threshold else False

    def add_to_pool(self):
        """补充代理
        :return: None
        """
        print('PoolAdder is working')
        spiders = [cls() for cls in SpiderMeta.spiders]
        flag = 0
        while not self.is_over():
            flag += 1
            raw_proxies = []
            with futures.ThreadPoolExecutor(max_workers=len(spiders)) as executor:
                future_to_down = {executor.submit(spiders[i].gets, 10): i for i in range(len(spiders))}
                for future in futures.as_completed(future_to_down):
                    raw_proxies.extend(future.result())
            print(raw_proxies)
            self._tester.set_raw_proxies(raw_proxies)
            self._tester.test()
            proxies = self._tester.usable_proxies
            if len(proxies) != 0:
                self._pool.puts(proxies)
            if self.is_over():
                break
            if flag >= 20:
                raise ResourceDepletionError
        for spider in spiders:
            spider.flush()

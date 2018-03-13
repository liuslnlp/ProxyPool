from . import UsabilityTester
from . import PoolAdder
from ..dbop import RedisOperator
from multiprocessing import Process
import time


class ExpireCheckProcess(Process):
    """过期性检验进程，每隔一段时间从 Pool 中提取出 1/4 的数据，检验
    其是否过期，没过期的重新入池，否则丢弃。
    """
    def __init__(self, cycle):
        """
        :param cycle: 扫描周期
        """
        Process.__init__(self)
        self._cycle = cycle

        self._tester = UsabilityTester()
        # self.daemon = True


    def run(self):
        pool = RedisOperator()
        print('Expire Check Process is working..')
        while True:
            time.sleep(self._cycle)
            total = int(0.25 * pool.size)
            if total < 4:
                continue
            raw_proxies = [pool.pop() for _ in range(total)]
            self._tester.set_raw_proxies(raw_proxies)
            self._tester.test()
            proxies = self._tester.usable_proxies
            if len(proxies) != 0:
                pool.puts(proxies)


class ProxyCountCheckProcess(Process):
    """proxy 数量监控进程，负责监控 Pool 中的代理数。当 Pool 中的
    代理数量低于下阈值时，将触发添加器，启动爬虫补充代理，当代理的数量
    打到上阈值时，添加器停止工作。
    """
    def __init__(self, lower_threshold, upper_threshold, cycle):
        """
        :param lower_threshold: 下阈值
        :param upper_threshold: 上阈值
        :param cycle: 扫描周期
        """
        Process.__init__(self)
        self._lower_threshold = lower_threshold
        self._upper_threshold = upper_threshold
        self._cycle = cycle

    def run(self):
        adder = PoolAdder()
        pool = RedisOperator()
        while True:
            if pool.size < self._lower_threshold:
                adder.add_to_pool()
            time.sleep(self._cycle)


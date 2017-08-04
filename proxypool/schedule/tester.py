import asyncio
import aiohttp


class UsabilityTester(object):
    """检验器，负责检验给定代理的可用性。"""
    test_api = 'https://www.baidu.com'

    def __init__(self):
        self.raw_proxies = None
        self._usable_proxies = None

    def set_raw_proxies(self, raw_proxies):
        self.raw_proxies = raw_proxies

        self._usable_proxies = []

    async def test_single_proxy(self, proxy):
        async with aiohttp.ClientSession() as sess:
            try:
                real_proxy = 'http://' + proxy
                async with sess.get(self.test_api, proxy=real_proxy, timeout=15) as resp:
                    self._usable_proxies.append(proxy)
            except Exception:
                print(Exception.__name__)

    def test(self):
        print('Usability tester is working...')
        loop = asyncio.get_event_loop()
        tasks = [self.test_single_proxy(proxy) for proxy in self.raw_proxies]
        loop.run_until_complete(asyncio.wait(tasks, loop=loop))

    @property
    def usable_proxies(self):
        return self._usable_proxies

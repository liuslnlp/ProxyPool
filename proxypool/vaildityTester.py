import asyncio
import aiohttp

class VaildityTester(object):
    

    test_api = 'https://www.baidu.com'

    """
    检验器，负责对未知的代理进行异步检测。
    """

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []
        self._loop = asyncio.get_event_loop()

    def set_raw_proxies(self, proxies):
        '''
        设置待检测的代理。
        '''
        self._raw_proxies = proxies
        self._usable_proxies = []

    async def test_single_proxy(self, proxy):
        '''
        检测一个代理，如果可用，则将其放入_usable_proxies中。
        '''
        async with aiohttp.ClientSession() as session:
            try:
                real_proxy = 'http://' + proxy
                async with session.get(self.test_api, proxy=real_proxy, timeout=15) as resp:
                    self._usable_proxies.append(proxy)
            except:
                pass

    def test(self):
        '''
        检测一组代理。
        '''
        tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
        self._loop.run_until_complete(asyncio.wait(tasks))

    def get_usable_proxies(self):
        '''
        将可用的代理返回。
        '''
        return self._usable_proxies

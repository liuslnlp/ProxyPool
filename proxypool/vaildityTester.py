import asyncio
import aiohttp

class VaildityTester(object):
    def __init__(self, raw_proxies=None):
        if raw_proxies == None:
            self.raw_proxies = []
        else:
            self.raw_proxies = raw_proxies
        self.usable_proxies = []
    
    def set_raw_proxies(self, proxies):
        self.raw_proxies.extend(proxies)

    
    def test(self):
        pass
    
    def get_usable_proxies(self):
        return self.usable_proxies

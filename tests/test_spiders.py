from proxypool.spiders import *
from proxypool.errors import RewriteSpiderError
import unittest

class SpiderTestCase(unittest.TestCase):
    def test_new(self):
        try:
            class TestSpider(metaclass=SpiderMeta):
                def gets(self):
                    pass

        except Exception:
            assert isinstance(Exception, RewriteSpiderError)

    def test_new2(self):
        try:
            class TestSpider(metaclass=SpiderMeta):
                pass

        except Exception:
            assert not isinstance(Exception, RewriteSpiderError)

    def test_new3(self):
        class TestSpiderA(metaclass=SpiderMeta):
            def gets(self):
                pass
        names = map(lambda cls: cls.__name__, SpiderMeta.spiders)
        assert TestSpiderA.__name__ in names

    def test_init(self):
        class TestSpiderB(metaclass=SpiderMeta):
            start_url = 'https://www.baidu.com'
            def gets(self):
                pass
        s = TestSpiderB()
        assert s._counter == 1
        s.increment(1)
        assert s._counter == 2
        s.increment(2)
        assert s._counter == 4
        s.flush()
        assert s._counter == 1

    def test_get(self):
        class TestSpiderC(metaclass=SpiderMeta):
            start_url = 'https://www.baidu.com'
            def gets(self):
                pass
        s = TestSpiderC()
        assert s.start_url == 'https://www.baidu.com'





if __name__ == '__main__':

    unittest.main()

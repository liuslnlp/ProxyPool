from proxypool.dbop import RedisOperator
import unittest


class RedisOperatorTestCase(unittest.TestCase):
    def setUp(self):
        self.opor = RedisOperator()

    def tearDown(self):
        self.opor._flush()

    def test_puts_and_pop(self):
        self.opor.puts('1')
        assert self.opor.pop() == '1'
        self.opor.puts(['1', '2', '3'])
        init_size = self.opor.size
        self.opor.pop()
        assert self.opor.size == init_size - 1

    def test_size(self):
        self.opor.puts(['1', '2', '3', '3'])
        assert self.opor.size == 3

    def test_gets(self):
        init_size = self.opor.size
        self.opor.gets(3)
        assert self.opor.size == init_size


if __name__ == '__main__':
    unittest.main()

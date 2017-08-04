from proxypool.webapi import app
from proxypool.dbop import RedisOperator
import unittest


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self._app = app.test_client()
        self._conn = RedisOperator()

    def tearDown(self):
        self._conn._flush()

    def test_get(self):
        self._conn.puts(['aaa'])
        self._conn.puts(['bbb'])
        r = self._app.get('/get')
        assert 'aaa' in str(r.data)

        r = self._app.get('/get')
        assert 'bbb' in str(r.data)

    def test_count(self):
        self._conn.puts(['aaa'])
        self._conn.puts(['bbb'])
        r = self._app.get('/count')
        assert '2' in str(r.data)
        self._conn.puts(['ccc'])
        self._conn.puts(['ddd'])
        r = self._app.get('/count')
        assert '4' in str(r.data)
        proxy = self._conn.pop()
        r = self._app.get('/count')
        assert '3' in str(r.data)


if __name__ == '__main__':
    unittest.main()

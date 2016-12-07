"""
数据库操作模块，负责与Redis的对接。
"""
import redis
from error import PoolEmptyError

HOST = 'localhost'
PORT = 6379


class RedisClient(object):

    def __init__(self):
        self.__db = redis.Redis(host=HOST, port=PORT)

    def get(self, count=1):
        proxies = self.__db.lrange("proxies", 0, count - 1)
        self.__db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        if self.__db.sadd("proxy_set", proxy):
            self.__db.rpush("proxies", proxy)
        else:
            pass

    def put_many(self, proxies):
        for proxy in proxies:
            self.put(proxy)

    def pop(self):
        # if self.queue_len == 0:
        #     pass
        try:
            return self.__db.blpop("proxies", 30)[1].decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        return self.__db.llen("proxies")

    def flush(self):
        self.__db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    conn.put("aaa")
    conn.put("bbb")

    print(conn.pop())
    print(conn.pop())
    print(conn.pop())
    conn.flush()

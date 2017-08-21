from .conf import HOST, PORT, POOL_NAME
import redis

redis_pool = redis.ConnectionPool(host=HOST, port=PORT, max_connections=20)


class RedisOperator(object):
    """Redis 操作类"""

    def __init__(self):
        """初始化 Redis 连接"""
        # self._conn = redis.Po(HOST, PORT)
        self._conn = redis.Redis(connection_pool=redis_pool)

    def gets(self, total=1):
        """从池中返回给定数量的代理(取出但不删除)，当 total > pool.size
        时，将返回 pool.size 个代理。
        :param total: 返回的数量
        :return: proxies, size=total
        """
        tmp = self._conn.srandmember(POOL_NAME, total)
        return [s.decode('utf-8') for s in tmp]

    def puts(self, proxies):
        """将一定量的代理压入 pool 中
        :param proxies:
        :return:
        """
        self._conn.sadd(POOL_NAME, *proxies)

    def pop(self):
        """弹出一个代理(取出并删除)
        :return: proxy
        """
        # if self.size == 0:
        #     raise PoolEmptyError
        return self._conn.spop(POOL_NAME).decode('utf-8')

    @property
    def size(self):
        """返回 pool 的 size
        :return: pool.size
        """
        return self._conn.scard(POOL_NAME)

    def _flush(self):
        """清空 Redis 中的全部内容
        :return: None
        """
        self._conn.flushall()


# Redis Host
HOST = 'localhost'
# Redis PORT
PORT = 6379

POOL_NAME = 'proxies'

POOL_LOWER_THRESHOLD = 10
POOL_UPPER_THRESHOLD = 40

VALID_CHECK_CYCLE = 600
POOL_LEN_CHECK_CYCLE = 20

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

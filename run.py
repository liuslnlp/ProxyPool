from proxypool.schedule import ProxyCountCheckProcess, ExpireCheckProcess
from proxypool.conf import VALID_CHECK_CYCLE, POOL_LEN_CHECK_CYCLE, \
    POOL_UPPER_THRESHOLD, POOL_LOWER_THRESHOLD
from proxypool.webapi import app

def cli():
    p1 = ProxyCountCheckProcess(POOL_LOWER_THRESHOLD, POOL_UPPER_THRESHOLD, POOL_LEN_CHECK_CYCLE)
    p2 = ExpireCheckProcess(VALID_CHECK_CYCLE)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    app.run()


if __name__ == '__main__':
    cli()

__author__ = 'WiseDoge'
__url__ = 'https://github.com/WiseDoge/ProxyPool'
__version__ = 'V2.0.0'


def main():
    """运行"""
    from .schedule import ProxyCountCheckProcess, ExpireCheckProcess
    from .conf import VALID_CHECK_CYCLE, POOL_LEN_CHECK_CYCLE, \
        POOL_UPPER_THRESHOLD, POOL_LOWER_THRESHOLD
    p1 = ProxyCountCheckProcess(POOL_LOWER_THRESHOLD, POOL_UPPER_THRESHOLD, POOL_LEN_CHECK_CYCLE)
    p2 = ExpireCheckProcess(VALID_CHECK_CYCLE)
    p1.start()
    p2.start()

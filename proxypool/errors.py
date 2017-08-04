class PoolEmptyError(Exception):
    """空池异常.
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy source is exhausted.')


class ResourceDepletionError(Exception):
    """资源枯竭异常，如果长时间抓取不到可用的
    代理，则触发此异常.
    """
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('There are not more proxies in internet.')


class RewriteSpiderError(Exception):
    """重写爬虫异常，当用户自己编写的爬虫类没有按照规定时，
    将触发此异常.
    """

    def __init__(self, cls_name):
        self.cls_name = cls_name
        Exception.__init__(self)

    def __str__(self):
        return repr(f'The spider `{self.cls_name}` does not has func `gets`.')

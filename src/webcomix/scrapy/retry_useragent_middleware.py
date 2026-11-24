from inspect import signature

from scrapy_fake_useragent.middleware import RetryUserAgentMiddleware as BaseMiddleware


class RetryUserAgentMiddleware(BaseMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler)
        middleware.crawler = crawler
        return middleware

    def _retry(self, request, reason, spider=None):
        retry = super()._retry
        if "spider" in signature(retry).parameters:
            return retry(request, reason, spider)
        return retry(request, reason)

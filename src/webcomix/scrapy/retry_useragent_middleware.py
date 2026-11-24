from scrapy.downloadermiddlewares.retry import RetryMiddleware, get_retry_request
from scrapy.utils.response import response_status_message
from scrapy_fake_useragent.middleware import RandomUserAgentBase


class RetryUserAgentMiddleware(RetryMiddleware, RandomUserAgentBase):
    def __init__(self, crawler):
        RetryMiddleware.__init__(self, crawler.settings)
        RandomUserAgentBase.__init__(self, crawler)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler)
        middleware.crawler = crawler
        return middleware

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status not in self.retry_http_codes:
            return response

        return (
            self._retry_with_new_user_agent(
                request, response_status_message(response.status), spider
            )
            or response
        )

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.exceptions_to_retry) and not request.meta.get(
            "dont_retry", False
        ):
            return self._retry_with_new_user_agent(request, exception, spider)
        return None

    def _retry_with_new_user_agent(self, request, reason, spider):
        request.headers["User-Agent"] = self._ua_provider.get_random_ua()
        return get_retry_request(
            request,
            spider=spider,
            reason=reason,
            max_retry_times=request.meta.get("max_retry_times", self.max_retry_times),
            priority_adjust=request.meta.get("priority_adjust", self.priority_adjust),
        )

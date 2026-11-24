from scrapy.downloadermiddlewares.retry import RetryMiddleware as BaseRetryMiddleware

from webcomix.scrapy.retry_useragent_middleware import (
    RetryUserAgentMiddleware as CompatibleRetryUserAgentMiddleware,
)


def test_retry_useragent_middleware_supports_scrapy_retry_signature(mocker):
    middleware = CompatibleRetryUserAgentMiddleware.__new__(
        CompatibleRetryUserAgentMiddleware
    )
    request = mocker.Mock()
    retry = mocker.patch.object(BaseRetryMiddleware, "_retry", return_value=request)

    result = middleware._retry(request, "503 Service Unavailable", mocker.Mock())

    assert result is request
    retry.assert_called_once_with(request, "503 Service Unavailable")


def test_from_crawler_sets_crawler_for_retry(mocker):
    crawler = mocker.Mock()
    mocker.patch.object(
        CompatibleRetryUserAgentMiddleware, "__init__", return_value=None
    )

    middleware = CompatibleRetryUserAgentMiddleware.from_crawler(crawler)

    assert middleware.crawler is crawler

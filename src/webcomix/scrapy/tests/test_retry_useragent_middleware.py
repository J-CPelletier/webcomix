import pytest
from scrapy.settings import Settings
from scrapy.http import HtmlResponse, Request

from webcomix.scrapy.retry_useragent_middleware import RetryUserAgentMiddleware
from scrapy_fake_useragent.middleware import RandomUserAgentBase


@pytest.fixture
def middleware(mocker):
    crawler = mocker.Mock()
    crawler.settings = Settings(
        {
            "RETRY_ENABLED": True,
            "RETRY_TIMES": 2,
            "RETRY_PRIORITY_ADJUST": -1,
            "RETRY_HTTP_CODES": [403, 500],
            "RETRY_EXCEPTIONS": [TimeoutError],
        }
    )
    user_agent_provider = mocker.Mock()
    user_agent_provider.get_random_ua.return_value = "rotated-agent"
    mocker.patch.object(
        RandomUserAgentBase, "_get_provider", return_value=user_agent_provider
    )
    crawler.stats = mocker.Mock()
    crawler.spider = mocker.Mock()
    middleware = RetryUserAgentMiddleware.from_crawler(crawler)
    return middleware


def test_retry_response_rotates_user_agent_and_uses_scrapy_retry_helper(
    mocker, middleware
):
    request = Request("https://example.com", headers={"User-Agent": "old-agent"})
    response = HtmlResponse(request.url, status=403, request=request)
    retry = mocker.patch(
        "webcomix.scrapy.retry_useragent_middleware.get_retry_request",
        return_value=request,
    )

    result = middleware.process_response(request, response, middleware.crawler.spider)

    assert result is request
    assert request.headers.get("User-Agent").decode() == "rotated-agent"
    retry.assert_called_once_with(
        request,
        spider=middleware.crawler.spider,
        reason="403 Forbidden",
        max_retry_times=2,
        priority_adjust=-1,
    )


def test_retry_exception_uses_scrapy_retry_helper(mocker, middleware):
    request = Request("https://example.com")
    retry = mocker.patch(
        "webcomix.scrapy.retry_useragent_middleware.get_retry_request",
        return_value=request,
    )

    result = middleware.process_exception(
        request, TimeoutError("timed out"), middleware.crawler.spider
    )

    assert result is request
    assert request.headers.get("User-Agent").decode() == "rotated-agent"
    retry.assert_called_once()


def test_non_retryable_response_is_returned_unchanged(mocker, middleware):
    request = Request("https://example.com")
    response = HtmlResponse(request.url, status=200, request=request)
    retry = mocker.patch("webcomix.scrapy.retry_useragent_middleware.get_retry_request")

    assert (
        middleware.process_response(request, response, middleware.crawler.spider)
        is response
    )
    retry.assert_not_called()


def test_dont_retry_request_is_returned_unchanged(mocker, middleware):
    request = Request("https://example.com", meta={"dont_retry": True})
    response = HtmlResponse(request.url, status=403, request=request)
    retry = mocker.patch("webcomix.scrapy.retry_useragent_middleware.get_retry_request")

    assert (
        middleware.process_response(request, response, middleware.crawler.spider)
        is response
    )
    retry.assert_not_called()

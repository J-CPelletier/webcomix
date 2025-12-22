import pytest
from scrapy.http import HtmlResponse, Request
from webcomix.scrapy.custom_cloudflare_middleware import CustomCloudflareMiddleware


AN_URL = "https://example.com/comic"
CLOUDFLARE_HTML = "<html><body>Cloudflare protected content</body></html>"


@pytest.fixture
def middleware():
    return CustomCloudflareMiddleware()


@pytest.fixture
def spider(mocker):
    spider = mocker.Mock()
    spider.logger = mocker.Mock()
    return spider


@pytest.fixture
def test_request():
    return Request(AN_URL)


def test_middleware_returns_response_when_status_200(middleware, test_request, spider):
    response = HtmlResponse(AN_URL, status=200, body=b"<html></html>")

    result = middleware.process_response(test_request, response, spider)

    assert result is response
    spider.logger.info.assert_not_called()


def test_middleware_returns_response_when_status_404(middleware, test_request, spider):
    response = HtmlResponse(AN_URL, status=404, body=b"<html></html>")

    result = middleware.process_response(test_request, response, spider)

    assert result is response
    spider.logger.info.assert_not_called()


def test_middleware_uses_cloudscraper_when_status_403(
    mocker, middleware, test_request, spider
):
    response = HtmlResponse(AN_URL, status=403, body=b"<html></html>")
    mock_cf_response = mocker.Mock()
    mock_cf_response.text = CLOUDFLARE_HTML
    mock_scraper = mocker.patch.object(CustomCloudflareMiddleware, "cloudflare_scraper")
    mock_scraper.get.return_value = mock_cf_response

    result = middleware.process_response(test_request, response, spider)

    mock_scraper.get.assert_called_once_with(AN_URL)
    assert isinstance(result, HtmlResponse)
    assert result.url == AN_URL
    assert CLOUDFLARE_HTML in result.text
    spider.logger.info.assert_called_once()


def test_middleware_uses_cloudscraper_when_status_503(
    mocker, middleware, test_request, spider
):
    response = HtmlResponse(AN_URL, status=503, body=b"<html></html>")
    mock_cf_response = mocker.Mock()
    mock_cf_response.text = CLOUDFLARE_HTML
    mock_scraper = mocker.patch.object(CustomCloudflareMiddleware, "cloudflare_scraper")
    mock_scraper.get.return_value = mock_cf_response

    result = middleware.process_response(test_request, response, spider)

    mock_scraper.get.assert_called_once_with(AN_URL)
    assert isinstance(result, HtmlResponse)
    assert result.url == AN_URL
    spider.logger.info.assert_called_once()


def test_middleware_logs_cloudflare_detection(mocker, middleware, test_request, spider):
    response = HtmlResponse(AN_URL, status=403, body=b"<html></html>")
    mock_cf_response = mocker.Mock()
    mock_cf_response.text = CLOUDFLARE_HTML
    mock_scraper = mocker.patch.object(CustomCloudflareMiddleware, "cloudflare_scraper")
    mock_scraper.get.return_value = mock_cf_response

    middleware.process_response(test_request, response, spider)

    spider.logger.info.assert_called_once_with(
        "Cloudflare detected. Using cloudscraper on URL: %s", AN_URL
    )


def test_middleware_returns_htmlresponse_with_utf8_encoding(
    mocker, middleware, test_request, spider
):
    response = HtmlResponse(AN_URL, status=503, body=b"<html></html>")
    mock_cf_response = mocker.Mock()
    mock_cf_response.text = CLOUDFLARE_HTML
    mock_scraper = mocker.patch.object(CustomCloudflareMiddleware, "cloudflare_scraper")
    mock_scraper.get.return_value = mock_cf_response

    result = middleware.process_response(test_request, response, spider)

    assert result.encoding == "utf-8"


def test_middleware_handles_different_urls(mocker, middleware, spider):
    different_url = "https://different-site.com/page"
    test_request = Request(different_url)
    response = HtmlResponse(different_url, status=403, body=b"<html></html>")
    mock_cf_response = mocker.Mock()
    mock_cf_response.text = CLOUDFLARE_HTML
    mock_scraper = mocker.patch.object(CustomCloudflareMiddleware, "cloudflare_scraper")
    mock_scraper.get.return_value = mock_cf_response

    result = middleware.process_response(test_request, response, spider)

    mock_scraper.get.assert_called_once_with(different_url)
    assert result.url == different_url

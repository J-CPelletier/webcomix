from scrapy import Request
from scrapy_splash import SplashRequest

from webcomix.scrapy.request_factory import RequestFactory


AN_URL = "https://xkcd.com"


def test_factory_creates_request_without_javascript(mocker):
    request_factory = RequestFactory(False, [])
    request = request_factory.create(AN_URL, mocker.ANY)
    assert isinstance(request, Request)


def test_factory_creates_splash_request_with_javascript(mocker):
    request_factory = RequestFactory(True, [])
    request = request_factory.create(AN_URL, mocker.ANY)
    assert isinstance(request, SplashRequest)


def test_factory_adds_cookies_to_request(mocker):
    request_factory = RequestFactory(True, [("foo", "bar")])
    request = request_factory.create(AN_URL, mocker.ANY)
    assert request.cookies == {"foo": "bar"}

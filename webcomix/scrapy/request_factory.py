from scrapy import Request
from scrapy_splash import SplashRequest


class RequestFactory:
    def __init__(self, javascript):
        self.javascript = javascript

    def create(self, url, next_page):
        if self.javascript:
            return SplashRequest(url, args={"wait": 0.5}, meta={"page": next_page})
        else:
            return Request(url, meta={"page": next_page})

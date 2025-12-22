from scrapy import Request
from scrapy_splash import SplashRequest


class RequestFactory:
    def __init__(self, javascript, cookies):
        self.javascript = javascript
        self.cookies = cookies

    def create(self, url, next_page):
        dict_cookies = {k: v for [k, v] in self.cookies}
        if self.javascript:
            return SplashRequest(
                url, args={"wait": 0.5}, cookies=dict_cookies, meta={"page": next_page}
            )
        else:
            return Request(url, meta={"page": next_page}, cookies=dict_cookies)

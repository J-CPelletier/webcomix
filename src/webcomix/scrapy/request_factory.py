from scrapy import Request


class RequestFactory:
    def __init__(self, javascript, cookies):
        self.javascript = javascript
        self.cookies = cookies

    def create(self, url, next_page):
        dict_cookies = {k: v for [k, v] in self.cookies}
        meta = {"page": next_page}

        if self.javascript:
            # Import lazily so non-JS runs don't require scrapy-playwright.
            from scrapy_playwright.page import PageMethod

            meta.update(
                {
                    "playwright": True,
                    # Match previous Splash behavior (args={"wait": 0.5})
                    "playwright_page_methods": [PageMethod("wait_for_timeout", 500)],
                }
            )

        return Request(url, meta=meta, cookies=dict_cookies)

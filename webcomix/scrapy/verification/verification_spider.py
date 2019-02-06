from urllib.parse import urljoin

from scrapy import Spider
from scrapy_splash import SplashRequest

from webcomix.exceptions import NextLinkNotFound
from webcomix.scrapy.verification.web_page import WebPage


class VerificationSpider(Spider):
    name = "Verification Spider"

    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.get("start_urls") or []
        self.next_page_selector = kwargs.get("next_page_selector", None)
        self.comic_image_selector = kwargs.get("comic_image_selector", None)
        self.number_of_pages_to_check = kwargs.get("number_of_pages_to_check", 3)
        super(VerificationSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        comic_image_urls = response.xpath(self.comic_image_selector).extract()
        page = response.meta.get("page") or 1
        image_urls = [
            urljoin(response.url, image_element_url)
            for image_element_url in comic_image_urls
        ]
        next_page_url = response.xpath(self.next_page_selector).extract_first()
        if page >= self.number_of_pages_to_check:
            yield WebPage(url=response.url, page=page, image_urls=image_urls)
            return
        elif next_page_url is not None and not next_page_url.endswith("#"):
            yield WebPage(url=response.url, page=page, image_urls=image_urls)
            yield SplashRequest(
                response.urljoin(next_page_url),
                args={
                    "wait": 0.5,
                },
                meta={
                    "page": page + 1,
                }
            )
        else:
            raise NextLinkNotFound(response.url, self.next_page_selector)

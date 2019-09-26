from urllib.parse import urljoin

from scrapy import Spider

from webcomix.exceptions import CrawlerBlocked, NextLinkNotFound
from webcomix.scrapy.request_factory import RequestFactory
from webcomix.scrapy.util import is_not_end_of_comic
from webcomix.scrapy.verification.web_page import WebPage


class VerificationSpider(Spider):
    name = "Verification Spider"

    def __init__(self, *args, **kwargs):
        self.start_url = kwargs.get("start_url")
        self.next_page_selector = kwargs.get("next_page_selector", None)
        self.comic_image_selector = kwargs.get("comic_image_selector", None)
        self.number_of_pages_to_check = kwargs.get("number_of_pages_to_check", 3)
        javascript = kwargs.get("javascript", False)
        self.alt_text_selector = kwargs.get("alt_text")
        self.request_factory = RequestFactory(javascript)
        super(VerificationSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield self.request_factory.create(url=self.start_url, next_page=1)

    def parse(self, response):
        comic_image_urls = response.xpath(self.comic_image_selector).getall()
        page = response.meta.get("page") or 1
        image_urls = [
            urljoin(response.url, image_element_url.strip())
            for image_element_url in comic_image_urls
        ]
        alt_text = (
            response.xpath(self.alt_text_selector).get()
            if self.alt_text_selector is not None
            else None
        )
        next_page_url = response.xpath(self.next_page_selector).get()
        if page >= self.number_of_pages_to_check:
            yield WebPage(
                url=response.url, page=page, image_urls=image_urls, alt_text=alt_text
            )
            return
        elif is_not_end_of_comic(next_page_url):
            yield WebPage(
                url=response.url, page=page, image_urls=image_urls, alt_text=alt_text
            )
            yield self.request_factory.create(
                url=response.urljoin(next_page_url).strip(), next_page=page + 1
            )
        else:
            raise NextLinkNotFound(response.url, self.next_page_selector)

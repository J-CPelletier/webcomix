from urllib.parse import urljoin

import scrapy

from webcomix.web_page import WebPage


class VerificationSpider(scrapy.Spider):
    name = "Verification Spider"

    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.get("start_urls") or []
        self.next_page_selector = kwargs.get("next_page_selector", None)
        self.comic_image_selector = kwargs.get("comic_image_selector", None)
        super(VerificationSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        comic_image_urls = response.xpath(self.comic_image_selector).extract()
        page = response.meta.get("page") or 1
        if page > 3:
            return
        image_urls = [
            urljoin(response.url, image_element_url)
            for image_element_url in comic_image_urls
        ]
        next_page_url = response.xpath(self.next_page_selector).extract_first()
        if next_page_url is not None and not next_page_url.endswith("#"):
            yield WebPage(url=response.url, page=page, image_urls=image_urls)
            yield scrapy.Request(
                response.urljoin(next_page_url), meta={"page": page + 1}
            )
        else:
            raise Exception(
                """\n
                    Next page XPath: {}\n
                    Image XPath: {}\n
                    Failed on URL: {}""".format(
                    self.next_page_selector, self.comic_image_selector, response.url
                )
            )

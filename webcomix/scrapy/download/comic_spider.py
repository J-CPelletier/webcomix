from urllib.parse import urljoin

import click
from scrapy import Spider

from webcomix.scrapy.download.comic_page import ComicPage
from webcomix.scrapy.request_factory import RequestFactory
from webcomix.scrapy.util import is_not_end_of_comic


class ComicSpider(Spider):
    name = "Comic Spider"

    def __init__(self, *args, **kwargs):
        self.start_url = kwargs.get("start_url")
        self.next_page_selector = kwargs.get("next_page_selector", None)
        self.comic_image_selector = kwargs.get("comic_image_selector", None)
        self.directory = kwargs.get("directory", None)
        javascript = kwargs.get("javascript", False)
        self.alt_text = kwargs.get("alt_text", None)
        self.title = kwargs.get("title", False)
        self.request_factory = RequestFactory(javascript)
        super(ComicSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield self.request_factory.create(url=self.start_url, next_page=1)

    def parse(self, response):
        click.echo("Downloading page {}".format(response.url))
        comic_image_urls = response.xpath(self.comic_image_selector).getall()
        page = response.meta.get("page") or 1
        alt_text = (
            response.xpath(self.alt_text).get() if self.alt_text is not None else None
        )
        for index, comic_image_url in enumerate(comic_image_urls):
            yield ComicPage(
                url=urljoin(response.url, comic_image_url.strip()),
                page=page + index,
                title=self.title,
                alt_text=alt_text,
            )
        if not comic_image_urls:
            click.echo("Could not find comic image.")
        next_page_url = response.xpath(self.next_page_selector).get()
        if is_not_end_of_comic(next_page_url):
            yield self.request_factory.create(
                url=response.urljoin(next_page_url).strip(),
                next_page=page + len(comic_image_urls),
            )

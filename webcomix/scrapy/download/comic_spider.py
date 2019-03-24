from urllib.parse import urljoin

import click
from scrapy import Spider
from scrapy_splash import SplashRequest

from webcomix.scrapy.download.comic_page import ComicPage


class ComicSpider(Spider):
    name = "Comic Spider"

    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.get("start_urls") or []
        self.next_page_selector = kwargs.get("next_page_selector", None)
        self.comic_image_selector = kwargs.get("comic_image_selector", None)
        self.directory = kwargs.get("directory", None)
        super(ComicSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        click.echo("Downloading page {}".format(response.url))
        comic_image_urls = response.xpath(self.comic_image_selector).getall()

        page = response.meta.get("page") or 1
        for index, comic_image_url in enumerate(comic_image_urls):
            yield ComicPage(
                url=urljoin(response.url, comic_image_url.strip()), page=page + index
            )
        if not comic_image_urls:
            click.echo("Could not find comic image.")
        next_page_url = response.xpath(self.next_page_selector).get()
        if next_page_url is not None and not next_page_url.endswith("#"):
            yield SplashRequest(
                response.urljoin(next_page_url).strip(),
                args={"wait": 0.5},
                meta={"page": page + 1},
            )

from urllib.parse import urljoin

import scrapy


class ComicSpider(scrapy.Spider):
    name = "My spider"

    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.get('start_urls') or []
        self.next_page_selector = kwargs.get('next_page_selector', None)
        self.comic_image_selector = kwargs.get('comic_image_selector', None)
        super(ComicSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        comic_image_url = response.xpath(
            self.comic_image_selector).extract_first()

        page = response.meta.get('page') or 1
        yield {
            "image_element": urljoin(response.url, comic_image_url),
            "page": page
        }
        next_page_url = response.xpath(self.next_page_selector).extract_first()
        if next_page_url is not None and not next_page_url.endswith('#'):
            yield scrapy.Request(
                response.urljoin(next_page_url), meta={'page': page + 1})

class VerificationSpider:
    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.get("start_urls") or []
        self.next_page_selector = kwargs.get("next_page_selector", None)
        self.comic_image_selector = kwargs.get("comic_image_selector", None)
        super(ComicSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        comic_image_urls = response.xpath(self.comic_image_selector).extract()
        page = response.meta.get("page") or 1
        if (page > 3):
            return
        for index, comic_image_url in enumerate(comic_image_urls):
            yield WebPage(url=urljoin(response.url, comic_image_url), page=page + index)
        next_page_url = response.xpath(self.next_page_selector).extract_first()
        if next_page_url is not None and not next_page_url.endswith("#") and comic_image_urls:
            yield scrapy.Request(
                response.urljoin(next_page_url),
                meta={"page": page + len(comic_image_urls)},
            )
        else:
            raise Exception(
                    """\n
                    Next page XPath: {}\n
                    Image XPath: {}\n
                    Failed on URL: {}""".format(
                        self.next_page_selector, self.comic_image_selector, url
                    )
                )

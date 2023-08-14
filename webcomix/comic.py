import os
from typing import Optional, List, Mapping, Dict, Any
from urllib.parse import urlparse
from zipfile import ZipFile, BadZipFile

import click

from webcomix.scrapy.download.comic_spider import ComicSpider
from webcomix.scrapy.verification.verification_spider import VerificationSpider
from webcomix.scrapy.crawler_worker import CrawlerWorker
from webcomix.scrapy.verification.web_page import WebPage

SPLASH_SETTINGS = {
    "SPLASH_URL": "http://0.0.0.0:8050",
    "DOWNLOADER_MIDDLEWARES": {
        "scrapy_splash.SplashCookiesMiddleware": 723,
        "scrapy_splash.SplashMiddleware": 725,
        "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
    },
    "SPIDER_MIDDLEWARES": {"scrapy_splash.SplashDeduplicateArgsMiddleware": 100},
    "DUPEFILTER_CLASS": "scrapy_splash.SplashAwareDupeFilter",
    "HTTPCACHE_STORAGE": "scrapy_splash.SplashAwareFSCacheStorage",
}

FAKE_USERAGENT_SETTINGS = {
    "DOWNLOADER_MIDDLEWARES": {
        "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
        "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
        "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
        "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
    },
    "FAKEUSERAGENT_PROVIDERS": [
        "scrapy_fake_useragent.providers.FakeUserAgentProvider",
        "scrapy_fake_useragent.providers.FakerProvider",
        "scrapy_fake_useragent.providers.FixedUserAgentProvider",
    ],
    "FAKEUSERAGENT_FALLBACK": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}


class Comic:
    def __init__(
        self,
        name: str,
        start_url: str,
        comic_image_selector: str,
        next_page_selector: str,
        start_page: int = 1,
        alt_text: Optional[str] = None,
        single_page: bool = False,
        delay: int = 0,
        javascript: bool = False,
        title: bool = False,
        debug: bool = False,
    ):
        self.name = name
        self.start_url = start_url
        self.start_page = start_page
        self.next_page_selector = next_page_selector
        self.comic_image_selector = comic_image_selector
        self.alt_text = alt_text
        self.single_page = single_page
        self.delay = delay
        self.javascript = javascript
        self.title = title
        self.debug = debug

    def download(self) -> None:
        """
        Downloads an entire comic page by page starting from the first one
        and saves them in the directory_name created in the current working
        directory
        """
        if not os.path.isdir(self.name):
            os.makedirs(self.name)

        settings = {
            **FAKE_USERAGENT_SETTINGS,
            "ITEM_PIPELINES": {
                "webcomix.scrapy.download.comic_pipeline.ComicPipeline": 1,
                "scrapy.pipelines.files.FilesPipeline": 500,
            },
            "LOG_ENABLED": self.debug,
            "FILES_STORE": self.name,
            "MEDIA_ALLOW_REDIRECTS": True,
            "RETRY_HTTP_CODES": [500, 502, 503, 504, 522, 524, 403, 408, 429],
            "DOWNLOAD_DELAY": self.delay,
        }  # type: Dict

        if self.javascript:
            settings.update(SPLASH_SETTINGS)

        worker = CrawlerWorker(
            settings,
            False,
            ComicSpider,
            start_url=self.start_url,
            start_page=self.start_page,
            comic_image_selector=self.comic_image_selector,
            next_page_selector=self.next_page_selector,
            directory=self.name,
            javascript=self.javascript,
            title=self.title,
            alt_text=self.alt_text,
        )

        worker.start()

        click.echo("Finished downloading the images.")

    def convert_to_cbz(self) -> None:
        """
        Takes all of the previously downloaded pages and compresses them in
        a .cbz file, erasing them afterwards.
        """
        with ZipFile("{}.cbz".format(self.name), mode="a") as cbz_file:
            images = os.listdir(self.name)
            for image in images:
                image_location = "{}/{}".format(self.name, image)
                cbz_file.write(image_location, image)
                os.remove(image_location)
            os.rmdir(self.name)
            if cbz_file.testzip() is not None:
                raise BadZipFile(
                    "Error while testing the archive; it might be corrupted."
                )

    def verify_xpath(self) -> List[Mapping[str, WebPage]]:
        """
        Takes a url and the XPath expressions for the next_page and image to
        go three pages into the comic. It returns a tuple containing the url
        of each page and their respective image urls.
        """
        settings = {
            **FAKE_USERAGENT_SETTINGS,
            "LOG_ENABLED": self.debug,
        }  # type: Dict[str, Any]

        if self.javascript:
            settings.update(SPLASH_SETTINGS)

        worker = CrawlerWorker(
            settings,
            True,
            VerificationSpider,
            start_url=self.start_url,
            comic_image_selector=self.comic_image_selector,
            next_page_selector=self.next_page_selector,
            number_of_pages_to_check=1 if self.single_page else 3,
            javascript=self.javascript,
            alt_text=self.alt_text,
        )

        verification = worker.start()

        return verification

    @staticmethod
    def save_image_location(
        url: str, page: int, directory_name: str = "", title: bool = False
    ) -> str:
        """
        Returns the relative location in the filesystem under which the
        webcomic will be saved. If directory_name is specified, it will be
        relative to the current directory; if not specified, it will return
        the name relative to the directory in which it is downloaded.
        """
        file_name = Comic.save_image_filename(url, page, title, directory_name)
        return os.path.join(directory_name, file_name)

    @staticmethod
    def save_image_filename(
        url: str, page: int, title_present: bool = False, comic_name: str = ""
    ) -> str:
        """
        Returns the filename of the comic image depending on whether or not we
        want it the comic's name to be present.
        """
        if url.count(".") <= 1:
            # No file extension (only dot in url is domain name)
            return str(page)

        parsed_filepath = urlparse(url).path
        file_extension = parsed_filepath[parsed_filepath.rindex(".") :]
        if title_present:
            return "{}-{}{}".format(comic_name, page, file_extension)
        else:
            return "{}{}".format(page, file_extension)

    @staticmethod
    def save_alt_text_location(page: int, directory_name: str = "") -> str:
        """
        Returns the relative location in the filesystem under which the comic
        image's alt text will be saved
        """
        file_name = str.format("{}.txt", page)
        return os.path.join(directory_name, file_name)

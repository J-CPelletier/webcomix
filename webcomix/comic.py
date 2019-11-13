import os
from typing import List, Mapping
from urllib.parse import urlparse
from zipfile import ZipFile, BadZipFile

import click
from fake_useragent import UserAgent

from webcomix.scrapy.download.comic_spider import ComicSpider
from webcomix.scrapy.verification.verification_spider import VerificationSpider
from webcomix.scrapy.crawler_worker import CrawlerWorker

user_agent = UserAgent()

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


class Comic:
    def __init__(
        self,
        name: str,
        start_url: str,
        comic_image_selector: str,
        next_page_selector: str,
        alt_text: str = None,
        single_page: bool = False,
        javascript: bool = False,
        title: bool = False,
    ):
        self.name = name
        self.start_url = start_url
        self.next_page_selector = next_page_selector
        self.comic_image_selector = comic_image_selector
        self.alt_text = alt_text
        self.single_page = single_page
        self.javascript = javascript
        self.title = title

    def download(self) -> None:
        """
        Downloads an entire comic page by page starting from the first one
        and saves them in the directory_name created in the current working
        directory
        """
        if not os.path.isdir(self.name):
            os.makedirs(self.name)

        settings = {
            "ITEM_PIPELINES": {
                "webcomix.scrapy.download.comic_pipeline.ComicPipeline": 1,
                "scrapy.pipelines.files.FilesPipeline": 500,
            },
            "LOG_ENABLED": False,
            "FILES_STORE": self.name,
            "MEDIA_ALLOW_REDIRECTS": True,
            "USER_AGENT": user_agent.chrome,
        }

        if self.javascript:
            settings.update(SPLASH_SETTINGS)

        worker = CrawlerWorker(
            settings,
            False,
            ComicSpider,
            start_url=self.start_url,
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

    def verify_xpath(self) -> List[Mapping]:
        """
        Takes a url and the XPath expressions for the next_page and image to
        go three pages into the comic. It returns a tuple containing the url
        of each page and their respective image urls.
        """
        settings = {"LOG_ENABLED": False, "USER_AGENT": user_agent.chrome}

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

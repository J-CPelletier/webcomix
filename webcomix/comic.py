import os
from urllib.parse import urljoin
from zipfile import ZipFile, BadZipFile

import click
import requests
from fake_useragent import UserAgent
from lxml import html
from scrapy.crawler import CrawlerProcess

from webcomix.comic_spider import ComicSpider

ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


class Comic:
    def __init__(self, start_url: str, next_page_selector: str,
                 comic_image_selector: str):
        self.start_url = start_url
        self.next_page_selector = next_page_selector
        self.comic_image_selector = comic_image_selector

    def download(self, directory_name: str = "finalComic"):
        """
        Downloads an entire Webcomic page by page starting from the first one
        and saves them in the directory_name created in the current working
        directory
        """
        if not os.path.isdir(directory_name):
            os.makedirs(directory_name)

        process = CrawlerProcess({
            'ITEM_PIPELINES': {
                'webcomix.comic_pipeline.ComicPipeline': 500,
                'scrapy.pipelines.files.FilesPipeline': 1
            },
            'LOG_ENABLED': False,
            'FILES_STORE': directory_name,
            'MEDIA_ALLOW_REDIRECTS': True
        })
        process.crawl(
            ComicSpider,
            start_urls=[self.start_url],
            next_page_selector=self.next_page_selector,
            comic_image_selector=self.comic_image_selector,
            directory=directory_name)
        process.start()

        click.echo("Finished downloading the images.")

    @staticmethod
    def save_image_location(url: str, page: int, directory_name: str = ''):
        """
        Returns the relative location in the filesystem under which the
        webcomic will be saved. If directory_name is specified, it will be
        relative to the current directory; if not specified, it will return
        the name relative to the directory in which it is downloaded.
        """
        if url.count(".") <= 1:
            # No file extension (only dot in url is domain name)
            file_name = str(page)
        else:
            file_name = "{}{}".format(page, url[url.rindex("."):])
        return os.path.join(directory_name, file_name)

    @staticmethod
    def make_cbz(comic_name: str, source_directory: str = "finalComic"):
        """
        Takes all of the previously downloaded pages and compresses them in
        a .cbz file, erasing them afterwards.
        """
        with ZipFile("{}.cbz".format(comic_name), mode="w") as cbz_file:
            images = os.listdir(source_directory)
            for image in images:
                image_location = "{}/{}".format(source_directory, image)
                cbz_file.write(image_location, image)
                os.remove(image_location)
            os.rmdir(source_directory)
            if cbz_file.testzip() is not None:
                raise BadZipFile(
                    "Error while testing the archive; it might be corrupted.")

    @staticmethod
    def verify_xpath(url: str, next_page: str, image: str):
        """
        Takes a url and the XPath expressions for the next_page and image to
        go three pages into the comic. It returns a tuple containing the url
        of each page and their respective image urls.
        """
        verification = []
        for _ in range(3):
            response = requests.get(url, headers=header)
            parsed_html = html.fromstring(response.content)
            try:
                image_element = parsed_html.xpath(image)[0]
                next_link = parsed_html.xpath(next_page)[0]
            except IndexError:
                raise Exception("""\n
                    Next page XPath: {}\n
                    Image XPath: {}\n
                    Failed on URL: {}""".format(next_page, image, url))
            image_url = urljoin(url, image_element)
            verification.append((url, image_url))
            url = urljoin(url, next_link)
        return verification

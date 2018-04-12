import os
from urllib.parse import urljoin
from zipfile import ZipFile

import click
import requests
from lxml import html
from fake_useragent import UserAgent

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

        url = self.start_url
        page = 1
        while True:
            click.echo("Downloading page {}".format(url))
            response = requests.get(url, headers=header)
            parsed_html = html.fromstring(response.content)

            image_element = parsed_html.xpath(self.comic_image_selector)
            next_link = parsed_html.xpath(self.next_page_selector)

            if image_element == []:
                click.echo("Could not find comic image.")
            else:
                try:
                    image_url = urljoin(url, image_element[0])
                    self.save_image(image_url, directory_name, page)
                except:
                    click.echo("The image couldn't be downloaded.")

            page += 1
            if next_link == [] or next_link[0].endswith("#"):
                break
            url = urljoin(url, next_link[0])
        click.echo("Finished downloading the images.")

    def save_image(self, image_url: str, directory_name: str, page: int):
        """
        Gets the image from the image_url and saves it in the directory_name
        """
        click.echo("Saving image {}".format(image_url))
        res = requests.get(image_url, headers=header)
        res.raise_for_status()
        image_path = Comic.save_image_location(image_url, directory_name, page)
        if os.path.isfile(image_path):
            click.echo("The image was already downloaded. Skipping...")
        else:
            with open(image_path, 'wb') as image_file:
                image_file.write(res.content)

    @staticmethod
    def save_image_location(url: str, directory: str, page: int):
        """
        Returns the location in the filesystem under which the webcomic will
        be saved
        """
        if url.count(".") <= 1:
            # No file extension (only dot in url is domain name)
            file_name = str(page)
        else:
            file_name = "{}{}".format(page, url[url.rindex("."):])
        return "/".join([directory, file_name])

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
                cbz_file.write(image_location)
                os.remove(image_location)
            os.rmdir(source_directory)
            if cbz_file.testzip() is not None:
                click.echo(
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

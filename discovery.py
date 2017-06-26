import requests, os
import click
from lxml import html
from urllib.parse import urljoin
from zipfile import ZipFile
from comic import Comic
from main import print_verification

possible_next_page_xpath = ["next", "Next"]
possible_image_xpath = ["comic", "Comic"]

def discovery(url):
    for next_page in possible_next_page_xpath:
        for image in possible_image_xpath:
            next_page_xpath = "//*[@*[contains(., '{}')]]//@href".format(next_page)
            image_xpath = "//*[@*[contains(., '{}')]]//@src".format(image)
            try:
                print_verification(Comic.verify_xpath(url, next_page_xpath, image_xpath))
                click.echo("Verify that the links above are correct before proceeding")
                if click.confirm("Are you sure you want to proceed?"):
                    comic = Comic(url, next_page_xpath, image_xpath)
                    comic.download()
                else:
                    click.echo("----------------")
            except:
                continue
    click.echo("Discovery has failed.")

if __name__ == "__main__":
    discovery("https://xkcd.com/1/")

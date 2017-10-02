#! python3

import os
import requests
from lxml import html
from urllib.parse import urljoin
import click

from webcomictocbz.search import search
from webcomictocbz.comic import Comic
from webcomictocbz.supported_comics import supported_comics

@click.group()
@click.version_option()
def cli():
    pass

@cli.command()
def comics():
    """
    Show all predefined webcomics
    """
    comics_content = ["{}: {}".format(key, value[0]) for key, value in sorted(supported_comics.items())]

    click.echo("\n".join(comics_content))

@cli.command()
@click.argument("name", type=click.STRING)
@click.option("--make_cbz", default=False, is_flag=True, help="Output the comic as a cbz file")
def download(name, make_cbz):
    """
    Download a webcomic from the list of supported comics by name
    """
    if name in list(supported_comics.keys()):
        comic = Comic(*supported_comics[name])
        comic.download(name)
        if make_cbz:
            comic.make_cbz(name, name)

@cli.command()
@click.argument("name", type=click.STRING)
@click.option("--first_page_url", prompt=True, type=click.STRING, help="URL of the comic's first page")
@click.option("--make_cbz", default=False, is_flag=True, help="Output the comic as a cbz file")
def search(name, first_page_url, make_cbz):
    """
    Downloads a webcomic using a general XPath
    """
    comic = discovery(first_page_url)
    if comic is not None:
        validation = Comic.verify_xpath(comic.url, comic.next_page_selector, comic.comic_image_selector)
        print_verification(validation)
        click.echo("Verify that the links above are correct before proceeding.")
        if click.confirm("Are you sure you want to proceed?"):
            comic.download(name)
            if make_cbz:
                comic.make_cbz(name, name)

@cli.command()
@click.option("--comic_name", prompt=True, type=click.STRING, help="Name of the user-defined comic")
@click.option("--first_page_url", prompt=True, type=click.STRING, help="URL of the comic's first page")
@click.option("--next_page_xpath", prompt=True, type=click.STRING, help="XPath expression giving the url to the next page")
@click.option("--image_xpath", prompt=True, type=click.STRING, help="XPath expression giving the url to the image")
@click.option("--make_cbz", default=False, is_flag=True, help="Output the comic as a cbz file")
def custom(comic_name, first_page_url, next_page_xpath, image_xpath, make_cbz):
    """
    Download a user-defined webcomic
    """
    comic = Comic(first_page_url, next_page_xpath, image_xpath)
    validation = Comic.verify_xpath(comic.url, comic.next_page_selector, comic.comic_image_selector)
    print_verification(validation)
    click.echo("Verify that the links above are correct before proceeding.")
    if click.confirm("Are you sure you want to proceed?"):
        comic.download(comic_name)
        if make_cbz:
            comic.make_cbz(comic_name, comic_name)

def print_verification(validation):
    """
    Prints the verification given by the verify_xpath function
    """
    for i in range(3):
        click.echo("Page {}: \nPage URL: {}\nImage URL: {}\n".format(i+1, validation[i][0], validation[i][1]))

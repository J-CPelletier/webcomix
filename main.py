#! python3

import requests, os
from lxml import html
from urllib.parse import urljoin
import click

from comic import Comic

supported_comics = {
    "xkcd": ("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']//img/@src"),
    "Nedroid": ("http://nedroid.com/2005/09/2210-whee/", "//div[@class='nav-next']/a/@href", "//div[@id='comic']/img/@src"),
    "JL8": ("http://limbero.org/jl8/1", "//b[2]/a/@href", "//img/@src"),
    "SMBC": ("http://www.smbc-comics.com/comic/2002-09-05", "//a[@class='next']/@href", "//img[@id='cc-comic']/@src"),
    "Blindsprings": ("http://www.blindsprings.com/comic/blindsprings-cover-book-one", "//a[@class='next']/@href", "//img[@id='cc-comic']/@src")
}

@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def comics():
    """
    Show all predefined webcomics
    """
    comics_content = ["{}: {}".format(key, value[0]) for key, value in supported_comics.items()]

    click.echo("\n".join(comics_content))

@cli.command()
@click.argument("name",  type=click.STRING)
@click.option("--make_cbz", default=False, is_flag=True, help="Output the comic as a cbz file")
def download(name,  make_cbz):
    """
    Download a webcomic from the list of supported comics
    """
    if name in list(supported_comics.keys()):
        comic = Comic(*supported_comics[name])
        comic.download(name)
    if make_cbz:
        comic.make_cbz(name, name)

@cli.command()
@click.option("--comic_name", prompt=True, type=click.STRING)
@click.option("--first_page_url", prompt=True, type=click.STRING)
@click.option("--next_page_xpath", prompt=True, type=click.STRING)
@click.option("--image_xpath", prompt=True, type=click.STRING)
@click.option("--make_cbz", default=False, is_flag=True)
def custom(comic_name, first_page_url, next_page_xpath, image_xpath, make_cbz):
    """
    Download a user-defined webcomic
    """
    validation = verify_xpath(first_page_url, next_page_xpath, image_xpath)
    print_verification(validation)

    comic = Comic(first_page_url, next_page_xpath, image_xpath)
    click.echo("Verify that the links above are correct before proceeding.")
    if click.confirm("Are you sure you want to proceed?"):
        comic.download(comic_name)
    if make_cbz:
        comic.make_cbz(comic_name, comic_name)

def verify_xpath(url, next_page, image):
    verification = []
    for i in range(3):
        response = requests.get(url)
        parsed_html = html.fromstring(response.content)

        image_element = parsed_html.xpath(image)[0]
        image_url = urljoin(url, image_element)
        next_link = parsed_html.xpath(next_page)[0]
        verification.append((url, image_url))
        url = urljoin(url, next_link)
    return verification

def print_verification(validation):
    for i in range(3):
        print("Page {}: \nPage URL: {}\nImage URL: {}\n".format(i+1, validation[i][0], validation[i][1]))

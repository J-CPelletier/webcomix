#! python3

import requests, os
from lxml import html
from urllib.parse import urljoin
import click

from comic import Comic
from supported_comics import supported_comics

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
        click.echo("Page {}: \nPage URL: {}\nImage URL: {}\n".format(i+1, validation[i][0], validation[i][1]))

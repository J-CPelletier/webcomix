#! python3

import requests, os
from lxml import html
from urllib.parse import urljoin
import click

from comic import Comic

__version__ = 0.1

supported_comics = {
    "xkcd": ("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']//img/@src"),
    "TheFoxSister": ("http://thefoxsister.com/?id=1", "//a[@class='comic-nav-next']/@href", "//img[@id='comicimg']/@src"),
    "Nedroid": ("http://nedroid.com/2005/09/2210-whee/", "//div[@class='nav-next']/a/@href", "//div[@id='comic']/img/@src"),
    "JL8": ("http://jl8comic.tumblr.com/post/13372482444/jl8-1-by-yale-stewart-based-on-characters-in-dc", "//a[@class='next-button']/@href", "//figure[@class='photo-hires-item']//img/@src"),
    "SMBC": ("http://www.smbc-comics.com/comic/2002-09-05", "//a[@class='next']/@href", "//img[@id='cc-comic']/@src"),
    "Blindsprings": ("http://www.blindsprings.com/comic/blindsprings-cover-book-one", "//a[@class='next']/@href", "//img[@id='cc-comic']/@src")
}

misc = ["quit/exit: Leaves the command prompt of the program",
        "custom: Downloads a comic defined url and XPath selectors",
        "make cbz: Creates a .cbz file using the specified folder containing the comic's images."]

YES = ["YES", "Y"]
NO = ["NO", "N"]

@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def comics():
    """
    Show all predefined webcomics
    """
    comics_header = "\n_Comic_ \n"
    comics_content = ["{}: {}".format(key, value[0]) for key, value in supported_comics.items()]
    misc_header = "\n_Misc_ \n"

    print(comics_header + "\n".join(comics_content))
    print(misc_header + "\n".join(misc) + "\n")

@cli.group()
@click.argument("name", default="foo", type=click.STRING)
@click.option("--make_cbz", default=False, is_flag=True)
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
        comic.make_cbz(comic_name)

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

if __name__ == '__main__':
    cli(obj={})

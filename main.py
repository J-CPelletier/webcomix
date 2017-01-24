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
def cli():
    pass


@cli.command()
def list():
    comics_header = "\n_Comic_ \n"
    comics_content = ["{}: {}".format(key, value[0]) for key, value in supported_comics.items()]
    misc_header = "\n_Misc_ \n"

    print(comics_header + "\n".join(comics_content))
    print(misc_header + "\n".join(misc) + "\n")

@cli.command()
@click.argument("name")
@click.option("--make_cbz", is_flag=True)
@click.option("--custom", is_flag=True)
def download(name, custom, make_cbz):
    if name in list(supported_comics.keys()):
        comic = Comic(*supported_comics[name])
        comic.download(user_input)
        cbz_confirm = input("Do you want your images to be converted in the same .cbz archive?(y/n) ")
        if cbz_confirm.upper() in YES:
            comic.make_cbz(name, name)
    elif custom:
        first_url = input("URL of the first image of the comic: ")
        next_page_xpath = input("XPath selector giving the link to the next page: ")
        image_xpath = input("XPath selector giving the link of the image: ")

        validation = verify_xpath(first_url, next_page_xpath, image_xpath)
        print_verification(validation)

        comic = Comic(first_url, next_page_xpath, image_xpath)
        print("Verify that the links above are correct before proceeding.")
        confirmation = input("Are you sure you want to proceed?(y/n) ")
        if confirmation.upper() in YES:
            comic.download()
    if make_cbz:
        source_directory = input("What is the name of the folder this comic is in? ")
        name = input("What will be the name of this archive? ")
        if os.path.isdir(source_directory):
            Comic.make_cbz(name, source_directory)
        else:
            print("The specified folder was not found.")


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

#! python3

import click

from webcomix.comic import Comic
from webcomix.exceptions import CrawlerBlocked, NextLinkNotFound
from webcomix.search import discovery
from webcomix.supported_comics import supported_comics
from webcomix.docker import DockerManager


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def comics():
    """
    Shows all predefined comics
    """
    comics_content = [
        "{}: {}".format(key, value["start_url"])
        for key, value in sorted(supported_comics.items())
    ]

    click.echo("\n".join(comics_content))


@cli.command()
@click.argument("name", type=click.Choice(supported_comics.keys()))
@click.option(
    "--cbz", is_flag=True, default=False, help="Outputs the comic as a cbz file"
)
@click.option(
    "--title", is_flag=True, default=False, help="Add title of comic in image names"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Add debugging output"
)
def download(name, cbz, title, verbose):
    """
    Downloads a predefined comic by name
    """
    if name in list(supported_comics.keys()):
        comic = Comic(**supported_comics[name], title=title, debug=verbose)
        download_webcomic(comic, cbz)


@cli.command()
@click.argument("name", type=click.STRING)
@click.option(
    "--start-url",
    "--start_url",
    prompt=True,
    type=click.STRING,
    help="URL of the comic's first page",
)
@click.option(
    "--start-page",
    "--start_page",
    type=click.INT,
    default=1,
    help="Number of comic's first page to be downloaded",
)
@click.option(
    "--cbz", default=False, is_flag=True, help="Outputs the comic as a cbz file"
)
@click.option(
    "--single-page",
    "--single_page",
    default=False,
    is_flag=True,
    help="Downloads from a single webpage",
)
@click.option(
    "--javascript",
    "--js",
    "-j",
    default=False,
    is_flag=True,
    help="Renders javascript in the page (slower)",
)
@click.option(
    "--title", is_flag=True, default=False, help="Add title of comic in image names"
)
@click.option(
    "--alt-text",
    "-a",
    default=None,
    type=click.STRING,
    help="Optional XPath to fetch an additionnal text while scraping",
)
@click.option(
    "--yes", "-y", default=False, is_flag=True, help="Skips the verification prompt"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Add debugging output"
)
def search(
    name,
    start_url,
    start_page,
    cbz,
    single_page,
    javascript,
    title,
    alt_text,
    yes,
    verbose,
):
    """
    Downloads a webcomic using a general XPath
    """
    with DockerManager(javascript):
        comic, validation = discovery(
            name,
            start_url,
            start_page,
            alt_text,
            single_page,
            javascript,
            title,
            verbose,
        )
        if comic is not None:
            print_verification(validation)
            click.echo("Verify that the links above are correct.")
            if yes or click.confirm("Are you sure you want to proceed?"):
                download_webcomic(comic, cbz)


@cli.command()
@click.argument("name", type=click.STRING)
@click.option(
    "--start-url",
    "--start_url",
    prompt=True,
    type=click.STRING,
    help="URL of the comic's first page to be downloaded",
)
@click.option(
    "--start-page",
    "--start_page",
    type=click.INT,
    default=1,
    help="Number of comic's first page to be downloaded",
)
@click.option(
    "--image-xpath",
    "--image_xpath",
    prompt=True,
    type=click.STRING,
    help="XPath expression giving the url to the image",
)
@click.option(
    "--next-page-xpath",
    "--next_page_xpath",
    prompt=True,
    type=click.STRING,
    help="XPath expression giving the url to the next page",
)
@click.option(
    "--cbz", default=False, is_flag=True, help="Outputs the comic as a cbz file"
)
@click.option(
    "--single-page",
    "--single_page",
    "-s",
    default=False,
    is_flag=True,
    help="Downloads from a single webpage",
)
@click.option(
    "--javascript",
    "--js",
    "-j",
    default=False,
    is_flag=True,
    help="Renders javascript in the page (slower)",
)
@click.option(
    "--title", is_flag=True, default=False, help="Add title of comic in image names"
)
@click.option(
    "--alt-text",
    "-a",
    default=None,
    type=click.STRING,
    help="XPath to fetch an additionnal text while scraping",
)
@click.option(
    "--yes", "-y", default=False, is_flag=True, help="Skips the verification prompt"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Add debugging output"
)
def custom(
    name,
    start_url,
    start_page,
    next_page_xpath,
    image_xpath,
    cbz,
    single_page,
    javascript,
    title,
    alt_text,
    yes,
    verbose,
):
    """
    Downloads a user-defined webcomic
    """
    with DockerManager(javascript):
        comic = Comic(
            name,
            start_url,
            image_xpath,
            next_page_xpath,
            start_page,
            alt_text,
            single_page,
            javascript,
            title,
            verbose,
        )
        try:
            validation = comic.verify_xpath()
        except NextLinkNotFound as exception:
            click.echo(
                "Could not find next link of: {} \nwith next page XPath expression: {}".format(
                    exception.failed_url, exception.next_page_xpath
                )
            )
            click.echo(
                "Have you tried testing your XPath expression with 'scrapy shell'?"
            )
            raise click.Abort()
        try:
            print_verification(validation)
        except CrawlerBlocked as exception:
            click.echo("{} could not be accessed with webcomix.".format(name))
            click.echo(
                "Chances are the website you're trying to download images from doesn't want to be scraped."
            )
            raise click.Abort()
        click.echo("Verify that the links above are correct.")
        if yes or click.confirm("Are you sure you want to proceed?"):
            download_webcomic(comic, cbz)


def print_verification(validation):
    """
    Prints the verification given by the verify_xpath function
    """
    if validation is None:
        raise CrawlerBlocked()
    for item in sorted(validation, key=lambda x: x.get("page")):
        output = "Page {}:\nPage URL: {}\nImage URLs:\n{}\n".format(
            item.get("page"), item.get("url"), "\n".join(item.get("image_urls"))
        )
        if item.get("alt_text") is not None:
            output += "Alt text: {}\n".format(item.get("alt_text"))
        click.echo(output)


def download_webcomic(comic, cbz):
    comic.download()
    if cbz:
        comic.convert_to_cbz()

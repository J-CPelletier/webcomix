#! python3

import click

from webcomix.comic import Comic
from webcomix.exceptions import NextLinkNotFound
from webcomix.search import discovery
from webcomix.supported_comics import supported_comics


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
        "{}: {}".format(key, value[0])
        for key, value in sorted(supported_comics.items())
    ]

    click.echo("\n".join(comics_content))


@cli.command()
@click.argument("name", type=click.STRING)
@click.option(
    "--cbz", is_flag=True, default=False, help="Outputs the comic as a cbz file"
)
def download(name, cbz):
    """
    Downloads a predefined comic by name
    """
    if name in list(supported_comics.keys()):
        comic = Comic(name, *supported_comics[name])
        comic.download()
        if cbz:
            comic.convert_to_cbz()


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
    "--yes", "-y", default=False, is_flag=True, help="Skips the verification prompt"
)
def search(name, start_url, cbz, single_page, javascript, yes):
    """
    Downloads a webcomic using a general XPath
    """
    comic, validation = discovery(name, start_url, single_page, javascript)
    if comic is not None:
        print_verification(validation)
        click.echo("Verify that the links above are correct.")
        if yes or click.confirm("Are you sure you want to proceed?"):
            comic.download()
            if cbz:
                comic.convert_to_cbz()


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
    "--yes", "-y", default=False, is_flag=True, help="Skips the verification prompt"
)
def custom(
    name, start_url, next_page_xpath, image_xpath, cbz, single_page, javascript, yes
):
    """
    Downloads a user-defined webcomic
    """
    comic = Comic(
        name, start_url, image_xpath, next_page_xpath, single_page, javascript
    )
    try:
        validation = comic.verify_xpath()
    except NextLinkNotFound as exception:
        click.echo(
            "Could not find next link of: {} \nwith next page XPath expression: {}".format(
                exception.failed_url, exception.next_page_xpath
            )
        )
        click.echo("Have you tried testing your XPath expression with 'scrapy shell'?")
    else:
        print_verification(validation)
        click.echo("Verify that the links above are correct.")
        if yes or click.confirm("Are you sure you want to proceed?"):
            comic.download()
            if cbz:
                comic.convert_to_cbz()


def print_verification(validation):
    """
    Prints the verification given by the verify_xpath function
    """
    for item in sorted(validation, key=lambda x: x.get("page")):
        click.echo(
            "Page {}:\nPage URL: {}\nImage URLs:\n{}\n".format(
                item.get("page"), item.get("url"), "\n".join(item.get("image_urls"))
            )
        )

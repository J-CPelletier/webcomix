from webcomictocbz import main
import click
from click.testing import CliRunner
from urllib.parse import urljoin
from zipfile import ZipFile
import pytest, os, shutil, requests
from webcomictocbz.comic import Comic

def test_print_verification(capfd):
    verification = Comic.verify_xpath(*main.supported_comics["xkcd"])
    main.print_verification(verification)
    out, err = capfd.readouterr()
    assert out == "Page 1: \nPage URL: http://xkcd.com/1/\nImage URL: http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg\n\nPage 2: \nPage URL: http://xkcd.com/2/\nImage URL: http://imgs.xkcd.com/comics/tree_cropped_(1).jpg\n\nPage 3: \nPage URL: http://xkcd.com/3/\nImage URL: http://imgs.xkcd.com/comics/island_color.jpg\n\n"

def test_supported_comics():
    for comic_name, comic_info in main.supported_comics.items():
        first_pages = Comic.verify_xpath(*comic_info)
        assert len(set(first_pages)) == 3

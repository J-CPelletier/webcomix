import main
import click
from click.testing import CliRunner
from urllib.parse import urljoin
from zipfile import ZipFile
import pytest, os, shutil, requests

def test_verify_xpath():
    assert main.verify_xpath(*main.supported_comics["xkcd"]) == [('http://xkcd.com/1/', 'http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg'), ('http://xkcd.com/2/', 'http://imgs.xkcd.com/comics/tree_cropped_(1).jpg'), ('http://xkcd.com/3/', 'http://imgs.xkcd.com/comics/island_color.jpg')]


def test_print_verification(capfd):
    verification = main.verify_xpath(*main.supported_comics["xkcd"])
    main.print_verification(verification)
    out, err = capfd.readouterr()
    assert out == "Page 1: \nPage URL: http://xkcd.com/1/\nImage URL: http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg\n\nPage 2: \nPage URL: http://xkcd.com/2/\nImage URL: http://imgs.xkcd.com/comics/tree_cropped_(1).jpg\n\nPage 3: \nPage URL: http://xkcd.com/3/\nImage URL: http://imgs.xkcd.com/comics/island_color.jpg\n\n"

def test_download():
    runner = CliRunner()
    result = runner.invoke(main.download, ["foo"])
    assert result.exit_code == 0

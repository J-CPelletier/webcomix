import click
from click.testing import CliRunner
import pytest, os, shutil, requests
from webcomictocbz.comic import Comic
from webcomictocbz import discovery
from webcomictocbz.supported_comics import supported_comics
from webcomictocbz import main

def test_print_verification(capfd):
    verification = Comic.verify_xpath(*supported_comics["xkcd"])
    main.print_verification(verification)
    out, err = capfd.readouterr()
    assert out == "Page 1: \nPage URL: http://xkcd.com/1/\nImage URL: http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg\n\nPage 2: \nPage URL: http://xkcd.com/2/\nImage URL: http://imgs.xkcd.com/comics/tree_cropped_(1).jpg\n\nPage 3: \nPage URL: http://xkcd.com/3/\nImage URL: http://imgs.xkcd.com/comics/island_color.jpg\n\n"

def test_comics():
    runner = CliRunner()
    result = runner.invoke(main.comics)
    assert result.exit_code == 0
    assert len(result.output) > 0

def mock_download(comic, name):
    print(name)

first_comic = list(sorted(supported_comics.keys()))[0]

def test_good_download(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(Comic, "download", mock_download)
    result = runner.invoke(main.download, [first_comic])
    assert result.exit_code == 0
    assert result.output.strip() == first_comic


def test_bad_download(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(Comic, "download", mock_download)
    result = runner.invoke(main.download, ["foo"])
    assert result.exit_code == 0
    assert result.output == ""

def mock_make_cbz(comic_class, name, source_directory):
    print(".cbz created")

def test_good_download_makecbz(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(Comic, "download", mock_download)
    monkeypatch.setattr(Comic, "make_cbz", mock_make_cbz)
    result = runner.invoke(main.download, [first_comic, "--make_cbz"])
    assert result.exit_code == 0
    assert result.output.strip() == "\n".join([first_comic, ".cbz created"])

def test_bad_download_make_cbz(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(Comic, "download", mock_download)
    monkeypatch.setattr(Comic, "make_cbz", mock_make_cbz)
    result = runner.invoke(main.download, ["foo", "--make_cbz"])
    assert result.exit_code == 0
    assert result.output == ""


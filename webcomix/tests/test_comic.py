import shutil
from urllib.parse import urljoin
from zipfile import ZipFile, BadZipFile

import pytest

from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics


def test_save_image_location():
    assert Comic.save_image_location(
        "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", 1,
        "foo") == "foo/1.jpg"
    assert Comic.save_image_location("", 1, "bar") == "bar/1"


def test_urljoin():
    assert urljoin("http://xkcd.com/1/",
                   "//imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
                   ) == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
    assert urljoin("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
                   "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
                   ) == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"


def test_make_cbz(tmpdir):
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href",
                  "//div[@id='comic']/img/@src")
    tmpdir.mkdir("test")
    for i in range(1, 6):
        image_file = tmpdir.join("test/{}.txt".format(i))
        image_file.write("testing {}".format(i))
    comic.make_cbz("test", tmpdir.join("test").strpath)
    with ZipFile("test.cbz") as cbz_file:
        for i in range(1, 6):
            with cbz_file.open("{}.txt".format(i), "r") as image_file:
                assert str(
                    image_file.read()).strip("b'") == "testing {}".format(i)


def test_make_cbz_corrupted_archive(tmpdir, mocker, capfd):
    corrupted_archive = mocker.patch.object(
        ZipFile, 'testzip', return_value=mocker.ANY)
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href",
                  "//div[@id='comic']/img/@src")
    tmpdir.mkdir("test")
    for i in range(1, 6):
        image_file = tmpdir.join("test/{}.txt".format(i))
        image_file.write("testing {}".format(i))
    with pytest.raises(BadZipFile):
        comic.make_cbz("test", tmpdir.join("test").strpath)


def test_download(mocker):
    mock = mocker.patch('webcomix.comic.CrawlerProcess.start')
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href",
                  "//div[@id='comic']//img/@src")
    comic.download("test")
    assert mock.call_count == 1
    shutil.rmtree("test")


def test_verify_xpath():
    assert Comic.verify_xpath(*supported_comics["xkcd"]) == [
        ('http://xkcd.com/1/',
         ['http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg']),
        ('http://xkcd.com/2/',
         ['http://imgs.xkcd.com/comics/tree_cropped_(1).jpg']),
        ('http://xkcd.com/3/', ['http://imgs.xkcd.com/comics/island_color.jpg'])
    ]

import os
import shutil
from urllib.parse import urljoin
from zipfile import ZipFile

import requests

from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics


def test_save_image_location():
    assert Comic.save_image_location(
        "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", "foo",
        1) == "foo/1.jpg"
    assert Comic.save_image_location("", "bar", 1) == "bar/1"


def test_urljoin():
    assert urljoin("http://xkcd.com/1/",
                   "//imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
                   ) == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
    assert urljoin("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
                   "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
                   ) == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"


def test_save_image_no_image():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href",
                  "//div[@id='comic']/img/@src")
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.makedirs("test")
    comic.save_image("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
                     "test", 1)
    assert os.path.isfile("test/1.jpg")
    os.remove("test/1.jpg")
    os.rmdir("test")


def test_save_image_already_present(capfd):
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href",
                  "//div[@id='comic']/img/@src")
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.makedirs("test")
    with open("test/1.jpg", "w") as image_file:
        image_file.write("1")
    comic.save_image("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
                     "test", 1)
    out, err = capfd.readouterr()
    assert out == (
        "Saving image http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg\n"
        "The image was already downloaded. Skipping...\n")
    os.remove("test/1.jpg")
    os.rmdir("test")


def test_make_cbz():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href",
                  "//div[@id='comic']/img/@src")
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.makedirs("test")
    for i in range(1, 6):
        with open("test/{}.txt".format(i), "w") as image_file:
            image_file.write("testing {}".format(i))
    comic.make_cbz("test", "test")
    with ZipFile("test.cbz") as cbz_file:
        for i in range(1, 6):
            with cbz_file.open("test/{}.txt".format(i), "r") as image_file:
                assert str(
                    image_file.read()).strip("b'") == "testing {}".format(i)
    os.remove("test.cbz")


def test_download():
    if os.path.isdir("test"):
        shutil.rmtree("test")
    if os.path.isfile("test.cbz"):
        os.remove("test.cbz")
    comic = Comic("https://j-cpelletier.github.io/webcomix/1.html",
                  "//a/@href", "//img/@src")
    comic.download("test")
    for i in range(1, 3):
        with open("test/{}.jpeg".format(i), "rb") as result:
            expected = requests.get(
                "https://j-cpelletier.github.io/webcomix/{}.jpeg".format(i))
            assert expected.content == result.read()
    shutil.rmtree("test")


def test_verify_xpath():
    assert Comic.verify_xpath(*supported_comics["xkcd"]) == [
        ('http://xkcd.com/1/',
         'http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg'),
        ('http://xkcd.com/2/',
         'http://imgs.xkcd.com/comics/tree_cropped_(1).jpg'),
        ('http://xkcd.com/3/', 'http://imgs.xkcd.com/comics/island_color.jpg')
    ]

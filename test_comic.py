from comic import Comic
from urllib.parse import urljoin
from zipfile import ZipFile
import pytest, os, shutil

def test_save_image_location():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
    assert comic.save_image_location("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", "kappa") == os.getcwd() + "/kappa/1.jpg"
    assert comic.save_image_location("", "lol") == os.getcwd() + "/lol/1"

def test_urljoin():
    assert urljoin("http://xkcd.com/1/", "//imgs.xkcd.com/comics/barrel_cropped_(1).jpg") == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
    assert urljoin("http://ssp-comics.com/comics/toe?page=1", "/img/comics/toe/54b26778c1725894f48393baf84d3b30.jpg") == "http://ssp-comics.com/img/comics/toe/54b26778c1725894f48393baf84d3b30.jpg"
    assert urljoin("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg") == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"

def test_save_image_no_image():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.makedirs("test")
    comic.save_image("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", "test")
    assert os.path.isfile("test/1.jpg")
    os.remove("test/1.jpg")
    os.rmdir("test")

def test_save_image_already_image(capfd):
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.makedirs("test")
    with open("test/1.jpg", "w") as image_file:
        image_file.write("1")
    comic.save_image("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", "test")
    out, err = capfd.readouterr()
    assert out == "Saving image http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg\n" + "The image was already downloaded. Skipping...\n"
    os.remove("test/1.jpg")
    os.rmdir("test")

def test_make_cbz():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
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
                assert str(image_file.read()).strip("b'") == "testing {}".format(i)
    os.remove("test.cbz")

from comic import Comic
from urllib.parse import urljoin
import pytest, os

def test_get_image_location():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
    assert comic.get_image_location("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg") == "{}{}{}{}".format(os.getcwd(), "finalComic", 1, ".jpg")
    assert comic.get_image_location("") == "{}{}{}".format(os.getcwd(), "finalComic", 1)

def test_urljoin():
    assert urljoin("http://xkcd.com/1/", "//imgs.xkcd.com/comics/barrel_cropped_(1).jpg") == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
    assert urljoin("http://ssp-comics.com/comics/toe?page=1", "/img/comics/toe/54b26778c1725894f48393baf84d3b30.jpg") == "http://ssp-comics.com/img/comics/toe/54b26778c1725894f48393baf84d3b30.jpg"
    assert urljoin("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg", "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg") == "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"

from comic import Comic
import pytest, os

def test_get_image_location():
    comic = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
    assert comic.get_image_location("http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg") == "{}{}{}{}".format(os.getcwd(), "finalComic", 1, ".jpg")
    assert comic.get_image_location("") == "{}{}{}".format(os.getcwd(), "finalComic", 1)

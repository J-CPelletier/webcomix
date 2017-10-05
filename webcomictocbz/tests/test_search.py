from webcomictocbz.comic import Comic
from webcomictocbz.search import search


def test_search_searchable_website():
    searchable_website = search("https://xkcd.com/1/")
    assert searchable_website.url == "https://xkcd.com/1/"
    assert searchable_website.next_page_selector == "//*[@*[contains(., '{}')]]//@href".format("next")
    assert searchable_website.comic_image_selector == "//*[@*[contains(., '{}')]]//@src".format("comic")

def test_search_unsearchable_website():
    unsearchable_website = search("https://j-cpelletier.github.io/WebComicToCBZ/1.html")
    assert unsearchable_website == None

from webcomix.comic import Comic
from webcomix.search import discovery


def test_search_searchable_website():
    searchable_website = discovery("https://xkcd.com/1/")
    assert searchable_website.start_url == "https://xkcd.com/1/"
    assert searchable_website.next_page_selector == "//*[@*[contains(., '{}')]]//@href".format("next")
    assert searchable_website.comic_image_selector == "//*[@*[contains(., '{}')]]//@src".format("comic")

def test_search_unsearchable_website():
    unsearchable_website = discovery("https://j-cpelletier.github.io/webcomix/1.html")
    assert unsearchable_website == None

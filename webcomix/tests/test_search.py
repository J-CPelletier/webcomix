from webcomix.comic import Comic
from webcomix.search import discovery


def test_search_searchable_website():
    expected = Comic("http://xkcd.com/1/",
                     "//*[@*[contains(., 'next')]]//@href",
                     "//*[@*[contains(., 'comic')]]//@src")
    result = discovery("http://xkcd.com/1/")
    assert Comic.verify_xpath(
        expected.start_url, expected.next_page_selector,
        expected.comic_image_selector) == [
            ('http://xkcd.com/1/',
             'http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg'),
            ('http://xkcd.com/2/',
             'http://imgs.xkcd.com/comics/tree_cropped_(1).jpg'),
            ('http://xkcd.com/3/',
             'http://imgs.xkcd.com/comics/island_color.jpg')
        ]

    assert result.start_url == expected.start_url
    assert result.next_page_selector == expected.next_page_selector
    assert result.comic_image_selector == expected.comic_image_selector


def test_search_unsearchable_website():
    result = discovery("https://j-cpelletier.github.io/webcomix/1.html")
    assert result is None

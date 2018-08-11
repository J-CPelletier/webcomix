from webcomix.comic import Comic
from webcomix.search import discovery


def test_search_searchable_website():
    expected = Comic(
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
        "//*[@*[contains(., 'next')]]//@href",
        "//*[@*[contains(., 'comic')]]//@src")
    result = discovery(
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one")
    assert Comic.verify_xpath(
        expected.start_url, expected.next_page_selector,
        expected.comic_image_selector) == [
            ('http://www.blindsprings.com/comic/blindsprings-cover-book-one',
             ['http://www.blindsprings.com/comics/cover.jpg']),
            ('http://www.blindsprings.com/comic/blindsprings-page-one',
             ['http://www.blindsprings.com/comics/1430199037-TB_01_001.jpg']),
            ('http://www.blindsprings.com/comic/blindsprings-page-two',
             ['http://www.blindsprings.com/comics/1430198957-TB_01_002.jpg'])
        ]

    assert result.start_url == expected.start_url
    assert result.next_page_selector == expected.next_page_selector
    assert result.comic_image_selector == expected.comic_image_selector


def test_search_unsearchable_website():
    result = discovery("https://j-cpelletier.github.io/webcomix/1.html")
    assert result is None

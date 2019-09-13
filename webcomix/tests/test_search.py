from webcomix.comic import Comic
from webcomix.search import discovery
from webcomix.tests.fake_websites.fixture import one_webpage_searchable_uri


def test_search_searchable_website(mocker):
    expected = Comic(
        "Blindsprings",
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
        "//*[contains(translate(@src, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'comic')]//@src",
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'next')]//@href",
        False,
    )
    mocker.patch("webcomix.search.possible_image_xpath", ["comic"])
    mocker.patch("webcomix.search.possible_next_page_xpath", ["next"])
    mocker.patch("webcomix.search.possible_tags_image", ["*"])
    mocker.patch("webcomix.search.possible_tags_next", ["*"])
    mocker.patch("webcomix.search.possible_attributes_image", [".", "@src"])
    mocker.patch("webcomix.search.possible_attributes_next", ["@class"])
    mocker.patch("webcomix.util.check_first_pages")
    comic, result = discovery(
        "Blindsprings",
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
        False,
    )
    assert result == [
        {
            "page": 1,
            "url": "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
            "image_urls": ["http://www.blindsprings.com/comics/cover.jpg"],
        },
        {
            "page": 2,
            "url": "http://www.blindsprings.com/comic/blindsprings-page-one",
            "image_urls": [
                "http://www.blindsprings.com/comics/1430199037-TB_01_001.jpg"
            ],
        },
        {
            "page": 3,
            "url": "http://www.blindsprings.com/comic/blindsprings-page-two",
            "image_urls": [
                "http://www.blindsprings.com/comics/1430198957-TB_01_002.jpg"
            ],
        },
    ]

    assert comic.start_url == expected.start_url
    assert comic.next_page_selector == expected.next_page_selector
    assert comic.comic_image_selector == expected.comic_image_selector


def test_search_unsearchable_website(mocker):
    mocker.patch("webcomix.search.possible_image_xpath", [])
    mocker.patch("webcomix.search.possible_next_page_xpath", [])
    mocker.patch("webcomix.search.possible_tags_image", [])
    mocker.patch("webcomix.search.possible_tags_next", [])
    mocker.patch("webcomix.search.possible_attributes_image", [])
    mocker.patch("webcomix.search.possible_attributes_next", [])

    assert discovery("comic_name", "test", True) == (None, None)


def test_stopping_searching(mocker):
    expected = Comic(
        "Blindsprings",
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'next')]//@href",
        "//*[contains(translate(@src, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'comic')]//@src",
        False,
    )
    mocker.patch("webcomix.search.possible_image_xpath", ["comic"])
    mocker.patch("webcomix.search.possible_next_page_xpath", ["next"])
    mocker.patch("webcomix.search.possible_tags_image", ["div"])
    mocker.patch("webcomix.search.possible_tags_next", ["div"])
    mocker.patch("webcomix.search.possible_attributes_image", ["@rel"])
    mocker.patch("webcomix.search.possible_attributes_next", ["@class"])
    exit_called = mocker.patch("sys.exit")
    mocker.patch("webcomix.comic.Comic.verify_xpath", side_effect=KeyboardInterrupt)
    result = discovery(
        "Blindsprings",
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
        False,
    )
    assert exit_called.call_count == 1
    assert result == (None, None)


def test_can_find_single_page_correctly_while_searching(
    mocker, one_webpage_searchable_uri
):
    mocker.patch("webcomix.search.possible_image_xpath", ["image"])
    mocker.patch("webcomix.search.possible_next_page_xpath", ["next"])
    mocker.patch("webcomix.search.possible_tags_image", ["*"])
    mocker.patch("webcomix.search.possible_tags_next", ["*"])
    mocker.patch("webcomix.search.possible_attributes_image", ["@class"])
    mocker.patch("webcomix.search.possible_attributes_next", ["."])

    comic, result = discovery("test", one_webpage_searchable_uri, True)

    validation = comic.verify_xpath()

    assert len(result) == 1
    assert result == validation
    assert len(result[0]["image_urls"]) == 2

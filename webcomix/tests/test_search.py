from webcomix.comic import Comic
from webcomix.search import discovery
from webcomix.tests.fake_websites.fixture import (
    one_webpage_searchable_uri,
    three_webpages_uri,
    three_webpages_classes_uri,
)


def test_search_searchable_website(mocker, three_webpages_classes_uri):
    expected = Comic(
        "Blindsprings",
        three_webpages_classes_uri,
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'comic')]//@src",
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'next')]//@href",
    )
    mocker.patch("webcomix.search.possible_image_xpath", ["comic"])
    mocker.patch("webcomix.search.possible_next_page_xpath", ["next"])
    mocker.patch("webcomix.search.possible_tags_image", ["*"])
    mocker.patch("webcomix.search.possible_tags_next", ["*"])
    mocker.patch("webcomix.search.possible_attributes_image", ["@class"])
    mocker.patch("webcomix.search.possible_attributes_next", ["@class"])
    mocker.patch("webcomix.util.check_first_pages")
    comic, result = discovery("Blindsprings", three_webpages_classes_uri)

    three_webpages_classes_folder = three_webpages_classes_uri.strip("1.html")

    assert result == [
        {
            "page": 1,
            "url": three_webpages_classes_uri,
            "image_urls": [three_webpages_classes_folder + "1.jpeg"],
            "alt_text": None,
        },
        {
            "page": 2,
            "url": three_webpages_classes_folder + "2.html",
            "image_urls": [three_webpages_classes_folder + "2.jpeg"],
            "alt_text": None,
        },
        {
            "page": 3,
            "url": three_webpages_classes_folder + "3.html",
            "image_urls": [three_webpages_classes_folder + "3.jpeg"],
            "alt_text": None,
        },
    ]

    assert comic.start_url == expected.start_url
    assert comic.next_page_selector == expected.next_page_selector
    assert comic.comic_image_selector == expected.comic_image_selector


def test_search_unsearchable_website(mocker, three_webpages_uri):
    mocker.patch("webcomix.search.possible_image_xpath", ["comic"])
    mocker.patch("webcomix.search.possible_next_page_xpath", ["next"])
    mocker.patch("webcomix.search.possible_tags_image", ["*"])
    mocker.patch("webcomix.search.possible_tags_next", ["*"])
    mocker.patch("webcomix.search.possible_attributes_image", ["@class"])
    mocker.patch("webcomix.search.possible_attributes_next", ["@class"])

    assert discovery("test", three_webpages_uri) == (None, None)


def test_can_stop_searching(mocker, three_webpages_classes_uri):
    mocker.patch("webcomix.search.possible_image_xpath", ["comic"])
    mocker.patch("webcomix.search.possible_next_page_xpath", ["next"])
    mocker.patch("webcomix.search.possible_tags_image", ["div"])
    mocker.patch("webcomix.search.possible_tags_next", ["div"])
    mocker.patch("webcomix.search.possible_attributes_image", ["@rel"])
    mocker.patch("webcomix.search.possible_attributes_next", ["@class"])
    exit_called = mocker.patch("sys.exit")
    mocker.patch("webcomix.comic.Comic.verify_xpath", side_effect=KeyboardInterrupt)
    result = discovery("test", three_webpages_classes_uri)
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

    comic, result = discovery("test", one_webpage_searchable_uri, single_page=True)

    validation = comic.verify_xpath()

    assert len(result) == 1
    assert result == validation
    assert len(result[0]["image_urls"]) == 2

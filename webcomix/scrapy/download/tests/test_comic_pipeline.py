import os

from scrapy.exceptions import DropItem
import pytest

from webcomix.scrapy.download.comic_pipeline import ComicPipeline
from webcomix.scrapy.download.comic_page import ComicPage
from webcomix.supported_comics import supported_comics

first_comic = list(sorted(supported_comics.values()))[0]

expected_url_image = "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
expected_image_location = "test/1.jpg"
expected_image_filename = "1.jpg"


def test_get_media_requests_returns_good_request_when_file_not_present(mocker):
    mocker.patch("os.path.isfile", return_value=False)
    mock_spider_info = mocker.patch("scrapy.pipelines.media.MediaPipeline.SpiderInfo")
    mocker.patch(
        "webcomix.comic.Comic.save_image_location", return_value=expected_image_location
    )
    mocker.patch(
        "webcomix.comic.Comic.save_image_filename", return_value=expected_image_filename
    )
    pipeline = ComicPipeline(store_uri="foo")
    elements = list(
        pipeline.get_media_requests(
            ComicPage(url=expected_url_image, page=1, title=False, alt_text=None),
            mock_spider_info,
        )
    )
    request = elements[0]
    assert request.url == expected_url_image
    assert request.meta["image_file_name"] == expected_image_filename
    os.rmdir("foo")


def test_get_media_requests_drops_item_when_file_present(mocker):
    mocker.patch("os.path.isfile", return_value=True)
    mock_spider_info = mocker.patch("scrapy.pipelines.media.MediaPipeline.SpiderInfo")
    mocker.patch(
        "webcomix.comic.Comic.save_image_location", return_value=expected_image_location
    )
    pipeline = ComicPipeline(store_uri="foo")
    with pytest.raises(DropItem):
        list(
            pipeline.get_media_requests(
                ComicPage(url=expected_url_image, page=1, title=False, alt_text=None),
                mock_spider_info,
            )
        )
    os.rmdir("foo")


def test_get_media_requests_drops_item_when_file_present_in_zip(mocker):
    mocker.patch("os.path.isfile", side_effect=[False])
    mocker.patch(
        "webcomix.scrapy.download.comic_pipeline.ComicPipeline.image_in_zipfile",
        return_value=True,
    )
    mock_spider_info = mocker.patch("scrapy.pipelines.media.MediaPipeline.SpiderInfo")
    mocker.patch(
        "webcomix.comic.Comic.save_image_location", return_value=expected_image_location
    )
    pipeline = ComicPipeline(store_uri="foo")
    with pytest.raises(DropItem):
        list(
            pipeline.get_media_requests(
                ComicPage(url=expected_url_image, page=1, title=False, alt_text=None),
                mock_spider_info,
            )
        )
    os.rmdir("foo")


def test_item_completed_returns_item_when_file_downloaded(mocker):
    results = [(True, {"path": expected_image_location})]
    item = ComicPage()
    pipeline = ComicPipeline(store_uri="foo")

    result = pipeline.item_completed(results, item, mocker.ANY)

    assert result == item
    os.rmdir("foo")


def test_item_completed_returns_drops_when_file_not_downloaded(mocker):
    results = [(False, {})]
    item = ComicPage()
    pipeline = ComicPipeline(store_uri="foo")

    with pytest.raises(DropItem):
        pipeline.item_completed(results, item, mocker.ANY)
    os.rmdir("foo")


def test_file_path_is_image_path(mocker):
    mock_request = mocker.patch("scrapy.http.Request")
    mock_request.meta = {"image_file_name": expected_image_location}
    pipeline = ComicPipeline(store_uri="foo")
    file_path = pipeline.file_path(mock_request)
    assert file_path == expected_image_location
    os.rmdir("foo")


def test_image_not_in_zip_if_zip_does_not_exist(mocker):
    mocker.patch("os.path.isfile", return_value=False)
    assert ComicPipeline.image_in_zipfile(mocker.ANY, mocker.ANY) == False

import os

import pytest
from scrapy.exceptions import DropItem
from scrapy.utils.test import get_crawler

from webcomix.scrapy.download.comic_pipeline import ComicPipeline
from webcomix.scrapy.download.comic_page import ComicPage
from webcomix.supported_comics import supported_comics

first_comic = list(supported_comics.values())[0]

expected_url_image = "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
expected_image_location = "test/1.jpg"
expected_image_filename = "1.jpg"


def make_pipeline(store_uri="foo"):
    crawler = get_crawler(settings_dict={"FILES_STORE": store_uri})
    return ComicPipeline.from_crawler(crawler)


def test_get_media_requests_returns_good_request_when_file_not_present(mocker, tmp_path):
    mocker.patch("os.path.isfile", return_value=False)
    mock_spider_info = mocker.patch("scrapy.pipelines.media.MediaPipeline.SpiderInfo")
    mocker.patch(
        "webcomix.comic.Comic.save_image_location", return_value=expected_image_location
    )
    mocker.patch(
        "webcomix.comic.Comic.save_image_filename", return_value=expected_image_filename
    )
    pipeline = make_pipeline(str(tmp_path / "foo"))
    elements = list(
        pipeline.get_media_requests(
            ComicPage(url=expected_url_image, page=1, title=False, alt_text=None),
            mock_spider_info,
        )
    )
    request = elements[0]
    assert request.url == expected_url_image
    assert request.meta["image_file_name"] == expected_image_filename


def test_get_media_requests_drops_item_when_file_present(mocker, tmp_path):
    mocker.patch("os.path.isfile", return_value=True)
    mock_spider_info = mocker.patch("scrapy.pipelines.media.MediaPipeline.SpiderInfo")
    mocker.patch(
        "webcomix.comic.Comic.save_image_location", return_value=expected_image_location
    )
    pipeline = make_pipeline(tmp_path / "foo")
    with pytest.raises(DropItem):
        list(
            pipeline.get_media_requests(
                ComicPage(url=expected_url_image, page=1, title=False, alt_text=None),
                mock_spider_info,
            )
        )


def test_get_media_requests_drops_item_when_file_present_in_zip(mocker, tmp_path):
    mocker.patch("os.path.isfile", side_effect=[False])
    mocker.patch(
        "webcomix.scrapy.download.comic_pipeline.ComicPipeline.image_in_zipfile",
        return_value=True,
    )
    mock_spider_info = mocker.patch("scrapy.pipelines.media.MediaPipeline.SpiderInfo")
    mocker.patch(
        "webcomix.comic.Comic.save_image_location", return_value=expected_image_location
    )
    pipeline = make_pipeline(tmp_path / "foo")
    with pytest.raises(DropItem):
        list(
            pipeline.get_media_requests(
                ComicPage(url=expected_url_image, page=1, title=False, alt_text=None),
                mock_spider_info,
            )
        )


def test_item_completed_returns_item_when_file_downloaded(mocker, tmp_path):
    results = [(True, {"path": expected_image_location})]
    item = ComicPage()
    pipeline = make_pipeline(tmp_path / "foo")

    result = pipeline.item_completed(results, item, mocker.ANY)

    assert result == item


def test_item_completed_returns_drops_when_file_not_downloaded(mocker, tmp_path):
    results = [(False, {})]
    item = ComicPage()
    pipeline = make_pipeline(tmp_path / "foo")

    with pytest.raises(DropItem):
        pipeline.item_completed(results, item, mocker.ANY)


def test_file_path_is_image_path(mocker, tmp_path):
    mock_request = mocker.patch("scrapy.http.Request")
    mock_request.meta = {"image_file_name": expected_image_location}
    pipeline = make_pipeline(tmp_path / "foo")
    file_path = pipeline.file_path(mock_request)
    assert file_path == expected_image_location


def test_image_not_in_zip_if_zip_does_not_exist(mocker):
    mocker.patch("os.path.isfile", return_value=False)
    assert not ComicPipeline.image_in_zipfile(mocker.ANY, mocker.ANY)

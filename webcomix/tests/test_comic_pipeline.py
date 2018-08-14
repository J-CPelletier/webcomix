from scrapy.exceptions import DropItem
from scrapy.http import Request
import pytest

from webcomix.comic_pipeline import ComicPipeline
from webcomix.comic_page import ComicPage
from webcomix.supported_comics import supported_comics

first_comic = list(sorted(supported_comics.values()))[0]

expected_url_image = "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
expected_image_location = "test/1.jpg"


def test_get_media_requests_returns_good_request_when_file_not_present(mocker):
    mock_file_not_there = mocker.patch('os.path.isfile', return_value=False)
    mock_spider_info = mocker.patch(
        'scrapy.pipelines.media.MediaPipeline.SpiderInfo')
    mock_got_save_image = mocker.patch(
        'webcomix.comic.Comic.save_image_location',
        return_value=expected_image_location)
    pipeline = ComicPipeline(store_uri="foo")
    elements = list(
        pipeline.get_media_requests(
            ComicPage(url=expected_url_image, page=1), mock_spider_info))
    request = elements[0]
    assert request.url == expected_url_image
    assert request.meta['image_file_name'] == expected_image_location


def test_get_media_requests_drops_item_when_file_present(mocker):
    mock_file_here = mocker.patch('os.path.isfile', return_value=True)
    mock_spider_info = mocker.patch(
        'scrapy.pipelines.media.MediaPipeline.SpiderInfo')
    mock_got_save_image = mocker.patch(
        'webcomix.comic.Comic.save_image_location',
        return_value=expected_image_location)
    pipeline = ComicPipeline(store_uri="foo")
    with pytest.raises(DropItem):
        elements = list(pipeline.get_media_requests(
            ComicPage(url=expected_url_image, page=1), mock_spider_info))


def test_item_completed_returns_item_when_file_downloaded(mocker):
    results = [(True, {'path': expected_image_location})]
    item = ComicPage()
    pipeline = ComicPipeline(store_uri="foo")

    result = pipeline.item_completed(results, item, mocker.ANY)

    assert result == item


def test_item_completed_returns_drops_when_file_not_downloaded(mocker):
    results = [(False, {})]
    item = ComicPage()
    pipeline = ComicPipeline(store_uri="foo")

    with pytest.raises(DropItem):
        pipeline.item_completed(results, item, mocker.ANY)


def test_file_path_is_image_path(mocker):
    mock_request = mocker.patch(
        'scrapy.http.Request')
    mock_request.meta = {'image_file_name': expected_image_location}
    pipeline = ComicPipeline(store_uri="foo")
    file_path = pipeline.file_path(mock_request)
    assert file_path == expected_image_location

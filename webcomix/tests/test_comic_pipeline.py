from scrapy.exceptions import DropItem
import pytest

from webcomix.comic_pipeline import ComicPipeline
from webcomix.comic_page import ComicPage
from webcomix.supported_comics import supported_comics

first_comic = list(sorted(supported_comics.values()))[0]

expected_url_image = "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
expected_image_location = "test/1.jpg"


def test_comic_pipeline_returns_good_request_when_file_not_present(mocker):
    file_not_there = mocker.patch('os.path.isfile', return_value=False)
    spider_info = mocker.patch(
        'scrapy.pipelines.media.MediaPipeline.SpiderInfo')
    got_save_image = mocker.patch(
        'webcomix.comic.Comic.save_image_location',
        return_value=expected_image_location)
    pipeline = ComicPipeline(store_uri="foo")
    elements = list(
        pipeline.get_media_requests(
            ComicPage(url=expected_url_image, page=1), spider_info))
    request = elements[0]
    assert request.url == expected_url_image
    assert request.meta['image_path'] == expected_image_location


def test_comic_pipeline_drops_item_when_file_present(mocker):
    file_here = mocker.patch('os.path.isfile', return_value=True)
    spider_info = mocker.patch(
        'scrapy.pipelines.media.MediaPipeline.SpiderInfo')
    got_save_image = mocker.patch(
        'webcomix.comic.Comic.save_image_location',
        return_value=expected_image_location)
    pipeline = ComicPipeline(store_uri="foo")
    with pytest.raises(DropItem):
        elements = list(pipeline.get_media_requests(
            ComicPage(url=expected_url_image, page=1), spider_info))

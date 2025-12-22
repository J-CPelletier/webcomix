import pytest

from webcomix.exceptions import NextLinkNotFound
from webcomix.scrapy.crawler_worker import CrawlerWorker
from webcomix.scrapy.verification.verification_spider import VerificationSpider
from webcomix.tests.fake_websites.fixture import one_webpage_uri


def test_spider_raising_error_gets_raised_by_crawler_worker(one_webpage_uri):
    settings = {"LOG_ENABLED": False}
    worker = CrawlerWorker(
        settings,
        False,
        VerificationSpider,
        start_url=one_webpage_uri,
        next_page_selector="//div/@href",
        comic_image_selector="//img/@src",
        number_of_pages_to_check=2,
    )

    with pytest.raises(NextLinkNotFound):
        worker.start()

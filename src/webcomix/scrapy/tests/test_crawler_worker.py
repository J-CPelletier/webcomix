import signal
import pytest

from webcomix.exceptions import NextLinkNotFound
from webcomix.scrapy.crawler_worker import CrawlerWorker
from webcomix.scrapy.verification.verification_spider import VerificationSpider
from webcomix.tests.fake_websites.fixture import one_webpage_uri


def test_verification_spider_only_allows_configured_http_statuses():
    default_spider = VerificationSpider(start_url="https://example.com")
    smbc_spider = VerificationSpider(
        start_url="https://example.com", handle_httpstatus_list=[500]
    )

    assert default_spider.handle_httpstatus_list == []
    assert smbc_spider.handle_httpstatus_list == [500]


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


def test_exit_gracefully_calls_stop():
    """_exit_gracefully should set the kill flag and stop the child process if present."""
    worker = CrawlerWorker({}, False)

    class DummyProcess:
        def __init__(self):
            self.stopped = False

        def stop(self):
            self.stopped = True

    dummy = DummyProcess()
    worker.process = dummy

    worker._exit_gracefully(signal.SIGTERM, None)

    assert worker.kill_process.is_set()
    assert dummy.stopped


def test_start_raises_child_exception(monkeypatch):
    """If the child process put an Exception into the result queue, start() should re-raise it."""
    # Prevent real process forking/joining
    import multiprocessing

    monkeypatch.setattr(multiprocessing.Process, "start", lambda self: None)
    monkeypatch.setattr(multiprocessing.Process, "join", lambda self, *a, **k: None)

    worker = CrawlerWorker({}, False)
    # Use a local queue.Queue so get_nowait behaves synchronously in this process
    import queue as _queue

    worker.result_queue = _queue.Queue()
    # Simulate the child process reporting an exception
    worker.result_queue.put(ValueError("foo"))

    with pytest.raises(ValueError):
        worker.start()


def test_start_raises_exception_after_partial_results(monkeypatch):
    import multiprocessing
    import queue

    monkeypatch.setattr(multiprocessing.Process, "start", lambda self: None)
    monkeypatch.setattr(multiprocessing.Process, "join", lambda self, *a, **k: None)

    worker = CrawlerWorker({}, False)
    worker.result_queue = queue.Queue()
    worker.result_queue.put({"url": "https://example.com/1"})
    worker.result_queue.put(NextLinkNotFound("https://example.com/2", "//a/@href"))

    with pytest.raises(NextLinkNotFound):
        worker.start()


def test_start_raises_when_no_results_are_returned(monkeypatch):
    import multiprocessing

    monkeypatch.setattr(multiprocessing.Process, "start", lambda self: None)
    monkeypatch.setattr(multiprocessing.Process, "join", lambda self, *a, **k: None)

    worker = CrawlerWorker({}, True)

    with pytest.raises(RuntimeError, match="without returning any results"):
        worker.start()


def test_start_raises_keyboardinterrupt_when_killed(monkeypatch):
    """If kill_process is set the parent should raise KeyboardInterrupt after join."""
    import multiprocessing

    monkeypatch.setattr(multiprocessing.Process, "start", lambda self: None)
    monkeypatch.setattr(multiprocessing.Process, "join", lambda self, *a, **k: None)

    worker = CrawlerWorker({}, False)
    worker.kill_process.set()

    with pytest.raises(KeyboardInterrupt):
        worker.start()

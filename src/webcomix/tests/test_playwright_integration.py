import os
import pytest

from webcomix.comic import Comic
from webcomix.tests.fake_websites.fixture import playwright_pages_uri


def test_verify_xpath_playwright(playwright_pages_uri):
    # These tests are skipped by default to avoid requiring Playwright browsers
    # in all environments. To run locally or in CI, set RUN_PLAYWRIGHT_TESTS=1
    # and install the Playwright browsers with:
    #   uv run playwright install chromium
    if os.environ.get("RUN_PLAYWRIGHT_TESTS") != "1":
        pytest.skip(
            "Set RUN_PLAYWRIGHT_TESTS=1 and install Playwright browsers to run this test."
        )

    import threading
    import socketserver
    import http.server
    import urllib.parse
    from pathlib import Path

    # Serve the file:// pages over HTTP so scrapy-playwright will handle them.
    parsed = urllib.parse.urlparse(playwright_pages_uri)
    pages_dir = Path(urllib.parse.unquote(parsed.path)).parent

    Handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args, directory=str(pages_dir), **kwargs)
    server = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        start_url = f"http://{host}:{port}/1.html"
        comic = Comic(
            "test_playwright",
            start_url,
            "//img/@src",
            "//a/@href",
            single_page=False,
            javascript=True,
        )

        verification = comic.verify_xpath()
    finally:
        server.shutdown()
        server.server_close()
    assert len(verification) == 2
    assert verification[0]["image_urls"]
    assert any(
        url.endswith("/1.jpeg") or url.endswith("1.jpeg")
        for url in verification[0]["image_urls"]
    )

import pytest

from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics


@pytest.mark.slow
def test_supported_comics():
    for comic_name, comic_info in supported_comics.items():
        first_pages = Comic.verify_xpath(*comic_info)
        assert len(set(first_pages)) == 3

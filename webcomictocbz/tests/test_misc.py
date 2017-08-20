from webcomictocbz.comic import Comic
from webcomictocbz.supported_comics import supported_comics
import pytest

def test_supported_comics():
    for comic_name, comic_info in supported_comics.items():
        first_pages = Comic.verify_xpath(*comic_info)
        assert len(set(first_pages)) == 3

import pytest

from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics
from webcomix.util import check_first_pages


@pytest.mark.slow
@pytest.mark.parametrize("comic_name", list(supported_comics.keys()))
def test_supported_comics(comic_name):
    comic = Comic(comic_name, *supported_comics[comic_name])
    first_pages = comic.verify_xpath()
    check_first_pages(first_pages)

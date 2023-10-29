import pytest

from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics
from webcomix.util import check_first_pages


@pytest.mark.flaky(reruns=5, reruns_delay=60)
@pytest.mark.slow
@pytest.mark.parametrize("comic_name", supported_comics.keys())
def test_supported_comics(comic_name):
    comic = Comic(**supported_comics[comic_name], debug=True)
    first_pages = comic.verify_xpath()
    try:
        check_first_pages(first_pages)
    except AssertionError:
        print("Comic failed! First pages:")
        print(first_pages)
        assert False
        pytest.fail("Comic could not be fetched!")

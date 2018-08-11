import pytest

from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics


@pytest.mark.slow
def test_supported_comics():
    for comic_name, comic_info in supported_comics.items():
        first_pages = Comic.verify_xpath(*comic_info)
        page_links = set([page[0] for page in first_pages])
        assert len(page_links) == 3
        list_of_images = [page[1] for page in first_pages]
        image_links = [image for page in list_of_images for image in page]
        assert len(set(image_links)) == len(image_links)

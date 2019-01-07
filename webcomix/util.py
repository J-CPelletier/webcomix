def check_first_pages(first_pages):
    page_links = set([page.get("url") for page in first_pages])
    assert len(set(page_links)) == len(page_links)
    assert len(page_links) == len(first_pages)
    list_of_images = [page.get("image_urls") for page in first_pages]
    image_links = [image for page in list_of_images for image in page]
    assert len(set(image_links)) == len(image_links)
    assert len(image_links) >= len(first_pages)

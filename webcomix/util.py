def check_first_pages(first_pages):
    page_links = set([page.get("url") for page in first_pages])
    assert len(page_links) == 3
    list_of_images = [page.get("image_urls") for page in first_pages]
    image_links = [image for page in list_of_images for image in page]
    assert len(set(image_links)) == len(image_links)
    assert len(image_links) >= 3

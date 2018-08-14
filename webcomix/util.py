def check_first_pages(first_pages):
    page_links = set([page[0] for page in first_pages])
    assert len(page_links) == 3
    list_of_images = [page[1] for page in first_pages]
    image_links = [image for page in list_of_images for image in page]
    assert len(set(image_links)) == len(image_links)
    assert len(image_links) >= 3

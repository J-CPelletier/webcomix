def is_not_end_of_comic(next_page_url):
    return next_page_url is not None and not next_page_url.endswith("#")


def get_comic_images(response, comic_image_selector, block_selectors):
    blocked = any(
        len(response.xpath(selector).getall()) > 0 for selector in block_selectors
    )
    comic_image_urls = response.xpath(comic_image_selector).getall()
    return [] if blocked else comic_image_urls

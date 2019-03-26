def is_not_end_of_comic(next_page_url):
    return next_page_url is not None and not next_page_url.endswith("#")

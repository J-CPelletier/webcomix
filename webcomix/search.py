import click

from webcomix.comic import Comic

possible_next_page_xpath = ["next", "Next"]
possible_image_xpath = ["comic", "Comic"]


def discovery(url):
    click.echo("Looking for a path to the whole comic...")
    for next_page in possible_next_page_xpath:
        for image in possible_image_xpath:
            next_page_xpath = "//*[@*[contains(., '{}')]]//@href".format(
                next_page)
            image_xpath = "//*[@*[contains(., '{}')]]//@src".format(image)
            try:
                first_pages = Comic.verify_xpath(url, next_page_xpath,
                                                 image_xpath)
                assert len(set(first_pages)) == 3
                return Comic(url, next_page_xpath, image_xpath)
            except:
                continue
    click.echo("Search has failed.")
    return None

import click

from webcomix.comic import Comic

possible_next_page_xpath = ["next", "Next"]
possible_image_xpath = ["comic", "Comic", "image", "Image"]


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
                page_links = set([page[0] for page in first_pages])
                assert len(page_links) == 3
                list_of_images = [page[1] for page in first_pages]
                image_links = [
                    image for page in list_of_images for image in page
                ]
                assert len(set(image_links)) == len(image_links)
                assert len(image_links) >= 3
                return Comic(url, next_page_xpath, image_xpath)
            except:
                continue
    click.echo("Search has failed.")
    return None

import sys
from itertools import product
from typing import Optional, List, Tuple, Mapping

import click
from tqdm import tqdm

from webcomix.comic import Comic
from webcomix.util import check_first_pages

possible_next_page_xpath = ["next"]
possible_image_xpath = ["comic", "image"]
possible_tags_image = ["*", "img", "div"]
possible_tags_next = ["*", "a", "div", "li"]
possible_attributes_image = [".", "@src", "@class", "@id", "@alt"]
possible_attributes_next = [".", "text()", "@class", "@id", "@alt", "@rel"]


def discovery(
    name: str,
    url: str,
    alt_text: str = None,
    single_page: bool = False,
    javascript: bool = False,
    title: bool = False,
) -> Tuple[Optional[Comic], Optional[List[Mapping]]]:
    def to_lower_case(attribute):
        return (
            "translate({}, "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz')"
        ).format(attribute)

    click.echo("Looking for a path to the whole comic... (Ctrl-C to exit)")
    combinations = product(
        possible_next_page_xpath,
        possible_image_xpath,
        possible_tags_image,
        possible_tags_next,
        possible_attributes_image,
        possible_attributes_next,
    )
    total = (
        len(possible_next_page_xpath)
        * len(possible_image_xpath)
        * len(possible_tags_image)
        * len(possible_tags_next)
        * len(possible_attributes_image)
        * len(possible_attributes_next)
    )

    for next_page, image, tag_image, tag_next, attribute_image, attribute_next in tqdm(
        combinations, total=total
    ):
        next_page_xpath = "//{}[contains({}, '{}')]//@href".format(
            tag_next, to_lower_case(attribute_next), next_page
        )
        image_xpath = "//{}[contains({}, '{}')]//@src".format(
            tag_image, to_lower_case(attribute_image), image
        )
        try:
            comic = Comic(
                name,
                url,
                image_xpath,
                next_page_xpath,
                alt_text,
                single_page,
                javascript,
                title,
            )
            first_pages = comic.verify_xpath()
            check_first_pages(first_pages)
            return comic, first_pages
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            continue
    click.echo("Search has failed.")
    return None, None

#! python3

import requests, os
from lxml import html
from urllib.parse import urljoin

from comic import Comic

supported_comics = {
    "xkcd": ("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']//img/@src")
}

misc = ["quit/exit: Leaves the program", "custom: User-defined comic"]

while True:
    user_input = input("Which comic do you want to download?\n")

    if user_input.upper() == "HELP":
        # Print all of the comics supported and gives a link to their website
        comics_header = "\n_Comic_ \n"
        comics_content = ["{}: {}".format(key, value[0]) for key, value in supported_comics.items()]
        misc_header = "\n_Misc_ \n"

        print(comics_header + "\n".join(comics_content))
        print(misc_header + "\n".join(misc) + "\n")

    elif user_input in list(supported_comics.keys()):
        comic = Comic(*supported_comics[user_input])
        comic.download()
        break

    elif user_input.upper() == "CUSTOM":
        first_url = input("URL of the first image of the comic: ")
        next_page_xpath = input("XPath selector giving the link to the next page: ")
        image_xpath = input("XPath selector giving the link of the image: ")
        comic = Comic(first_url, next_page_xpath, image_xpath)
        confirmation = input("Are you sure you want to proceed?(y/n) ")
        if confirmation.upper() in ["YES", "Y"]:
            comic.download()
        elif confirmation.upper() in ["NO", "N"]:
            continue
        else:
            break

    elif user_input.upper() in ["QUIT", "EXIT"]:
        break

    else:
        print("This command does not exist. Use HELP for a list of available choices.\n")

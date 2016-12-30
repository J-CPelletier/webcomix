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

    elif user_input.upper() in ["QUIT", "EXIT"]:
        break

    else:
        print("This command does not exist. Use HELP for a list of available choices.\n")

#! python3

import requests, os
from lxml import html
from urllib.parse import urljoin

from comic import Comic

supported_comics = {
    "xkcd": ("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']//img/@src"),
    "TheFoxSister": ("http://thefoxsister.com/?id=1", "//a[@class='comic-nav-next']/@href", "//a[@class='comic-nav-next']/img/@src")
}

misc = ["quit/exit: Leaves the command prompt of the program",
        "custom: Downloads a comic defined url and XPath selectors",
        "make cbz: Creates a .cbz file using the specified folder containing the comic's images."]

YES = ["YES", "Y"]
NO = ["NO", "N"]

def main():
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
            comic.download(user_input)
            cbz_confirm = input("Do you want your images to be converted in the same .cbz archive?(y/n) ")
            if cbz_confirm.upper() in YES:
                comic.make_cbz(user_input, user_input)
            break

        elif user_input.upper() == "CUSTOM":
            first_url = input("URL of the first image of the comic: ")
            next_page_xpath = input("XPath selector giving the link to the next page: ")
            image_xpath = input("XPath selector giving the link of the image: ")

            validation = verify_xpath(first_url, next_page_xpath, image_xpath)
            print_verification(validation)

            comic = Comic(first_url, next_page_xpath, image_xpath)
            print("Verify the links above are correct before proceeding.")
            confirmation = input("Are you sure you want to proceed?(y/n) ")
            if confirmation.upper() in YES:
                comic.download()
            elif confirmation.upper() in NO:
                continue
            else:
                break

            cbz_confirm = input("Do you want your images to be converted in the same .cbz archive?(y/n) ")
            if cbz_confirm.upper() in YES:
                name = input("What will be the name of this archive? ")
                comic.make_cbz(name)
            break

        elif user_input.upper() == "MAKE CBZ":
            source_directory = input("What is the name of the folder this comic is in? ")
            name = input("What will be the name of this archive? ")
            if os.path.isdir(source_directory):
                Comic.make_cbz(name, source_directory)
            else:
                print("The specified folder was not found.")

        elif user_input.upper() in ["QUIT", "EXIT"]:
            break

        else:
            print("This command does not exist. Use HELP for a list of available choices.\n")


def verify_xpath(url, next_page, image):
    verification = []
    for i in range(3):
        response = requests.get(url)
        parsed_html = html.fromstring(response.content)

        image_element = parsed_html.xpath(image)[0]
        image_url = urljoin(url, image_element)
        next_link = parsed_html.xpath(next_page)[0]
        verification.append((url, image_url))
        url = urljoin(url, next_link)
    return verification

def print_verification(validation):
    for i in range(3):
        print("Page {}: \nPage URL: {}\nImage URL: {}\n".format(i+1, validation[i][0], validation[i][1]))


if __name__ == "__main__":
    main()

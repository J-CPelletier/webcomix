import requests, os
from lxml import html
from urllib.parse import urljoin

class Comic:
    def __init__(self, start_url, next_page_selector, comic_image_selector):
        self.url = start_url
        self.next_page_selector = next_page_selector
        self.comic_image_selector = comic_image_selector
        self.current_page = 1

    def download(self):
        os.makedirs("finalComic")
        while True:
            print("Downloading page {}".format(self.url))
            response = requests.get(self.url)
            parsed_html = html.fromstring(response.content)

            image_element = parsed_html.xpath(self.comic_image_selector)
            next_link = parsed_html.xpath(self.next_page_selector)

            if next_link == [] or self.url.endswith("#"):
                break
            elif image_element == []:
                print("Could not find comic image.")
            else:
                try:
                    image_url = urljoin(self.url,image_element[0])
                    self.save_image(image_url)
                except:
                    print("The image couldn't be downloaded.")
                    pass

            self.current_page += 1
            self.url = urljoin(self.url, next_link[0])
        print("Finished downloading the images.")

    def save_image(self, image_url):
        print("Saving image {}".format(image_url))
        res = requests.get(image_url)
        res.raise_for_status()

        # Save the image to ./finalComic
        with open(self.get_image_location(image_url), 'wb') as imageFile:
            imageFile.write(res.content)

    def get_image_location(self, comic_url):
        cwd = os.getcwd().rstrip("/")
        directory = "finalComic"
        if comic_url.count(".") <= 1:
            # No file extension
            file_name = str(self.current_page)
        else:
            file_name = "{}{}".format(self.current_page, comic_url[comic_url.rindex("."):])
        return "/".join([cwd, directory, file_name])


# Testing
# dummy = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']/img/@src")
# dummy.download()

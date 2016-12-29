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
            html = requests.get(self.url)
            parsed_html = lxml.html.fromstring(html.content)

            image_element = parsed_html.xpath(self.comic_image_selector)
            next_link = parsed_html.xpath(self.next_page_selector)

            if next_link == [] or self.url.endswith("#"):
                break
            elif image_element == []:
                print("Could not find comic image.")
            else:
                try:
                    image_url = self.urljoin(self.url,image_element)
                    self.save_image(image_url[0])
                except requests.exceptions.HTTPError:
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
        cwd = os.path.join(os.getcwd())
        directory = "finalComic"
        extension = os.path.splitext(os.path.basename(comic_url))[1]
        return "".join([cwd, directory, str(self.current_page), extension])

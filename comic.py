import requests, os
from lxml import html
from urllib.parse import urljoin
from zipfile import ZipFile

class Comic:

    CWD = os.getcwd()
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

            if image_element == []:
                print("Could not find comic image.")
            else:
                try:
                    image_url = urljoin(self.url,image_element[0])
                    self.save_image(image_url)
                except:
                    print("The image couldn't be downloaded.")
                    pass

            self.current_page += 1
            if next_link == [] or next_link[0].endswith("#"):
                break
            self.url = urljoin(self.url, next_link[0])
        print("Finished downloading the images.")

    def save_image(self, image_url):
        print("Saving image {}".format(image_url))
        res = requests.get(image_url)
        res.raise_for_status()

        # Save the image to ./finalComic
        with open(self.save_image_location(image_url), 'wb') as imageFile:
            imageFile.write(res.content)

    def save_image_location(self, url):
        cwd = self.CWD.rstrip("/")
        directory = "finalComic"
        if url.count(".") <= 1:
            # No file extension
            file_name = str(self.current_page)
        else:
            file_name = "{}{}".format(self.current_page, url[url.rindex("."):])
        return "/".join([cwd, directory, file_name])

    def make_cbz(self, comic_name):
        cbz_file = ZipFile("{}/{}.cbz".format(self.CWD, comic_name), mode="w")
        images = os.listdir(os.getcwd() + "/finalComic")
        for image in images:
            cbz_file.write(image)
        if cbz_file.testzip() != None:
            print("Error while testing the archive; it might be corrupted.")
            cbz_file.close()
        else:
            cbz_file.close()


# Testing
# dummy = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']//img/@src")
# dummy.download()
# dummy.makecbz("bob")

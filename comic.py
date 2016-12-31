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

    def download(self, directory_name="finalComic"):
        os.makedirs(directory_name)
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
                    image_url = urljoin(self.url, image_element[0])
                    self.save_image(image_url, directory_name)
                except:
                    print("The image couldn't be downloaded.")

            self.current_page += 1
            if next_link == [] or next_link[0].endswith("#"):
                break
            self.url = urljoin(self.url, next_link[0])
        print("Finished downloading the images.")

    def save_image(self, image_url, directory_name):
        print("Saving image {}".format(image_url))
        res = requests.get(image_url)
        res.raise_for_status()
        # Save the image
        with open(self.save_image_location(image_url, directory_name), 'wb') as imageFile:
            imageFile.write(res.content)

    def save_image_location(self, url, directory):
        cwd = self.CWD.rstrip("/")
        if url.count(".") <= 1:
            # No file extension
            file_name = str(self.current_page)
        else:
            file_name = "{}{}".format(self.current_page, url[url.rindex("."):])
        return "/".join([cwd, directory, file_name])

    def make_cbz(self, comic_name, source_directory="finalComic"):
        cbz_file = ZipFile("{}/{}.cbz".format(self.CWD, comic_name), mode="w")
        images = os.listdir(self.CWD + "/" + source_directory)
        for image in images:
            cbz_file.write("{}/{}".format(source_directory ,image))
            os.remove("{}/{}".format(source_directory, image))
        os.rmdir(source_directory)
        if cbz_file.testzip() != None:
            print("Error while testing the archive; it might be corrupted.")
            cbz_file.close()
        else:
            cbz_file.close()


# Testing
# dummy = Comic("http://xkcd.com/1/", "//a[@rel='next']/@href", "//div[@id='comic']//img/@src")
# dummy.download()
# dummy.makecbz("bob")

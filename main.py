#! python3

# This is where the main function will be executed.
import webbrowser, requests, os, bs4

def downloadComic(url):
    os.makedirsnal(finalComic, exists_ok = True) # The exists_ok = True prevents the program from giving us an exception when the folder exists
    while not url.endswith('#'):
        # TODO: Download the page
        print("Downloading page {}".format(url))

        html = requests.get(url)
        html.raise_for_status() # Raises an HTTPerror if something went wrong with the request
        parsedHTML = BeautifulSoup(html)
        # TODO: Find the URL of the comic page

        # TODO: Download the image

        # TODO: Save the image to ./finalComic

    print("Done.")

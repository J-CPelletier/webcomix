#! python3

# TODO: Make this work for any other comic than xkcd
import webbrowser, requests, os, urllib, bs4, pdb

def downloadComic(url):
    os.makedirs('finalComic') # The exists_ok = True prevents the program from giving us an exception when the folder exists
    while not url.endswith('#'):
        # Download the page
        print("Downloading page {}".format(url))
        html = requests.get(url)
        html.raise_for_status() # Raises an HTTPerror if something went wrong with the request
        parsedHTML = bs4.BeautifulSoup(html.text, 'html.parser')

        # Find the URL of the comic page
        comicElem = parsedHTML.select('#comic img') # The div selected must be different depending on the webPage it is taken from
        prevLink = parsedHTML.find_all("a", rel="prev")[0]
        if comicElem == []:
            print('Could not find comic image.')
        else:
            # TODO: Download the image
            try:
                comicURL = 'http:' + comicElem[0].get('src')
                print("Downloading image {}".format(comicURL))
                result = requests.get(comicURL)
                # result.raise_for_status()
                # a = parsedHTML.select("#middleContainer br")
                # pdb.set_trace()

                # TODO: Save the image to ./finalComic
                image = urllib.request.urlopen(comicURL)
                with open(os.path.join(os.getcwd(), 'finalComic', os.path.basename(comicURL)), 'wb') as imageFile:
                    imageFile.write(result.content)

            except:
                # Skip the comic
                print("kappa")
                url = "http://xkcd.com" + prevLink.get('href')
                continue

        # TODO: Get the "previous" button's URL
        url = 'http://xkcd.com' + prevLink.get('href')
    print("Done.")

downloadComic('http://xkcd.com/')

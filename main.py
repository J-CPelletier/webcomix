#! python3

# TODO: Make this work for any other comic than xkcd
import webbrowser, requests, os, urllib, bs4, pdb

def downloadComic(url):
    os.makedirs('finalComic')
    while not url.endswith('#'):
        # Download the page
        print("Downloading page {}".format(url))
        html = requests.get(url)
        html.raise_for_status() # Raises an HTTPerror if something went wrong with the request
        parsedHTML = bs4.BeautifulSoup(html.text, 'html.parser')

        # Find the URL of the comic page
        comicElem = parsedHTML.select('#comic img') # The div selected must be different depending on the webPage it is taken from
        nextLink = parsedHTML.find_all("a", rel="next")[0]
        if comicElem == []:
            print('Could not find comic image.')
        else:
            # Download the image
            try:
                comicURL = 'http:' + comicElem[0].get('src')
                print("Downloading image {}".format(comicURL))
                result = requests.get(comicURL)
                result.raise_for_status()
                # pdb.set_trace()
                # To get the comic's name, use os.path.basename(comicURL) instead of os.path.splitext(os.path.basename(comicURL))[1] (which only gives the extension)

                # Save the image to ./finalComic
                image = urllib.request.urlopen(comicURL)
                with open(os.path.join(os.getcwd(), 'finalComic', url.strip("http://xkcd.com/") + os.path.splitext(os.path.basename(comicURL))[1]), 'wb') as imageFile:
                    imageFile.write(result.content)

            except:
                # Skip the comic
                url = "http://xkcd.com" + nextLink.get('href')
                continue

        # Get the "previous" button's URL
        url = 'http://xkcd.com' + nextLink.get('href')
    print("Done.")

# downloadComic('http://xkcd.com/1/')
while True:
    comic = input("Which comic do you want to download?(use 'help' to see available choices) ")

    if comic == "help":
        # Print all of the comics supported and gives a link to their website
        comics = ["xkcd: http://xkcd.com/"
        ]

        misc = ["quit: Leaves the program"
        ]

        print("\n_Comics_ \n" + "\n".join(comics) + "\n \n_Misc_ \n" + "\n".join(misc))

    if comic == "xkcd":
        downloadComic('http://xkcd.com/1/')

    elif comic == "quit":
        break

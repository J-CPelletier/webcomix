# webcomix

[![Build Status](https://travis-ci.org/J-CPelletier/webcomix.svg?branch=master)](https://travis-ci.org/J-CPelletier/webcomix)[![Coverage Status](https://coveralls.io/repos/github/J-CPelletier/webcomix/badge.svg?branch=master)](https://coveralls.io/github/J-CPelletier/webcomix?branch=master)[![PyPI version](https://badge.fury.io/py/webcomix.svg)](https://badge.fury.io/py/webcomix)

## Description

webcomix is a webcomic downloader that can additionally create a .cbz (Comic Book ZIP) file once downloaded.

## Notice

This program is for personal use only. Please be aware that by making the downloaded comics publicly available without the permission of the author, you may be infringing upon various copyrights.

## Installation

### Dependencies

* Python (3.5 or newer)
* click
* fake-useragent
* scrapy (Some additional steps might be required to include this package and can be found [here](https://doc.scrapy.org/en/latest/intro/install.html#intro-install-platform-notes))
* scrapy-splash
* tqdm

### Process

#### End user

1. Install [Python 3](https://www.python.org/downloads/)
2. Install the command line interface tool with `pip install webcomix`

#### Developer

1. Install [Python 3](https://www.python.org/downloads/)
2. Clone this repository and open a terminal in its directory
3. Install [poetry](https://github.com/python-poetry/poetry) with `pip install poetry`
3. Download the dependencies by running `poetry install`
4. Install pre-commit hooks with `pre-commit install`

## Usage

`webcomix [OPTIONS] COMMAND [ARGS]`

### Global Flags

#### help

Show the help message and exit.

#### Version

Show the version number and exit.

### Commands

#### comics

Shows all predefined comics which can be used with the `download` command.

#### download

Downloads a predefined comic. Supports the `--cbz` flag, which creates a .cbz archive of the downloaded comic.

#### search

Searches for an XPath that can download the whole comic. Supports the `--cbz` flag, which creates a .cbz archive of the downloaded comic,`-s`, which verifies only the provided page of the comic, and `-y`, which skips the verification prompt.

#### custom

Downloads a user-defined comic. To download a specific comic, you'll need a link to the first page, an XPath expression giving out the link to the next page and an XPath expression giving out the link to the image. More info [here](http://www.w3schools.com/xml/xpath_syntax.asp). Supports the `--cbz` flag, which creates a .cbz archive of the downloaded comic, `-s`, which verifies only the provided page of the comic, and `-y`, which skips the verification prompt.

### Examples

* `webcomix download xkcd`
* `webcomix search xkcd --start-url=http://xkcd.com/1/`
* `webcomix custom --cbz` (You will be prompted about other needed arguments)
* `webcomix custom xkcd --start-url=http://xkcd.com/1/ --next-page-xpath="//a[@rel='next']/@href" --image-xpath="//div[@id='comic']//img/@src" --cbz` (Same as before, but with all arguments declared beforehand)

### Making an XPath selector

Using an HTML inspector, spot a html path to the next link's `href` attribute/comic image's `src` attribute.

e.g.: `//div[@class='foo']/img/@src`
This will select the src attribute of the first image whose class is: foo

Note: `webcomix` works best on static websites, since `scrapy`(the framework we use to travel web pages) doesn't process Javascript.

To make sure your XPath is correct, you have to go into `scrapy shell`, which should be downloaded when you've installed `webcomix`.

```
scrapy shell <website> --> Use the website's url to go to it.
> response.body --> Will give you the html from the website.
> response.xpath --> Test an xpath selection. If you get [], this means your XPath expression hasn't gotten anything from the webpage.
```

### Downloading comics on Javascript-heavy websites

If the webcomic's website uses javascript to render its images, you won't be able to download it using the default configuration. webcomix now has an optional flag `-j` on both the `custom` and `search` command to execute the javascript using [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash). In order to use it, you'll need to have [Docker](https://www.docker.com/) installed and run the following command before trying to download the comic:

```
docker run -p 8050:8050 scrapinghub/splash
```

## Contribution

The procedure depends on the type of contribution:

* If you simply want to request the addition of a comic to the list of supported comics, make an issue with the label "Enhancement".
* If you want to request the addition of a feature to the system or a bug fix, make an issue with the appropriate label.

### Running the tests

To run the tests, you have to use the `pytest` command in the webcomix folder.

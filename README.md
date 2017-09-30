# WebComicToCBZ

[![Build Status](https://travis-ci.org/J-CPelletier/WebComicToCBZ.svg?branch=master)](https://travis-ci.org/J-CPelletier/WebComicToCBZ)[![Coverage Status](https://coveralls.io/repos/github/J-CPelletier/WebComicToCBZ/badge.svg?branch=master)](https://coveralls.io/github/J-CPelletier/WebComicToCBZ?branch=master)

## Description

WebComicToCBZ is a Python-based web comic downloader that can additionally create a .cbz (Comic Book ZIP) file once downloaded.

## Notice

This program is for personal use only. Please be aware that by making the downloaded comics publicly available without the permission of the author, you may be infringing upon various copyrights.

## Installation

### Dependencies

* Python3
* lxml
* requests
* click
* PyQt5 (If you're using the Graphical User Interface version of this tool)

### Process

#### With the requirements.txt

1. Install [Python 3](https://www.python.org/downloads/)
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3. Clone this repository and open a terminal in its directory.
4. Get the required packages by running `pip install -r requirements.txt`
5. Install the command line interface tool with `pip install --editable .`

#### Without the requirements.txt

1. Install [Python 3](https://www.python.org/downloads/)
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3. Get lxml by running `pip install lxml` (More info [here](http://lxml.de/installation.html#where-to-get-it))
4. Get requests by running `pip install requests` (More info [here](http://docs.python-requests.org/en/master/user/install/))
5. Get click by running `pip install click` (More info [here](http://click.pocoo.org/5/quickstart/))
5. Clone this repository or download its ZIP and open a terminal in its directory.
6. Install the command line interface tool with `pip install --editable .`

## Usage

`WebComicToCBZ [OPTIONS] COMMAND [ARGS]`

### Global Flags

#### help

Show the help message and exit.

#### Version

Show the version number and exit.

### Commands

#### comics

Shows all predefined comics which can be used with the `download` command.

#### download

Downloads a predefined comic. Supports the `--make_cbz` flag, which creates a .cbz archive of the downloaded comic.

#### search

Searches for an XPath that can download the whole comic. Supports the `--make_cbz` flag, which creates a .cbz archive of the downloaded comic. 

#### custom

Downloads a user-defined comic. To download a specific comic, you'll need a link to the first page, an XPath expression giving out the link to the next page and an XPath expression giving out the link to the image. More info [here](http://www.w3schools.com/xml/xpath_syntax.asp). Supports the `--make_cbz` flag, which creates a .cbz archive of the downloaded comic.

### Examples

* `WebComicToCBZ download xkcd`
* `WebComicToCBZ search xkcd --first_page_url=http://xkcd.com/1/`
* `WebComicToCBZ custom --make_cbz` (You will be prompted about other needed arguments)
* `WebComicToCBZ custom --comic_name=xkcd --first_page_url=http://xkcd.com/1/ --next_page_xpath="//a[@rel='next']/@href" --image_xpath="//div[@id='comic']//img/@src" --make_cbz` (Same as before, but with all arguments declared beforehand)

### Making an XPath selector

Using an HTML inspector, spot a html path to the next link's `href` attribute/comic image's `src` attribute.

e.g.: `//div[@class='foo']/img/@src`
This will select the src attribute of the first image whose class is: foo

## Contribution

The procedure depends on the type of contribution:

* If you simply want to request the addition of a comic to the list of supported comics, make an issue with the label "Enhancement".
* If you want to request the addition of a feature to the system or a bug fix, make an issue with the appropriate label.

### Running the tests

To run the tests, you have to get pytest(with `pip install -U pytest`) and use the `pytest` command in the WebComicToCBZ folder.

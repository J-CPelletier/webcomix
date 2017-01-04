# WebComicToCBZ

[![Build Status](https://travis-ci.org/J-CPelletier/WebComicToCBZ.svg?branch=master)](https://travis-ci.org/J-CPelletier/WebComicToCBZ)

## Description

WebComicToCBZ is a Python-based web comic downloader that can additionally create a .cbz (Comic Book ZIP) file once downloaded.

## Installation

### Dependencies

* Python3
* lxml
* requests

### Process

1. Install [Python 3](https://www.python.org/downloads/)
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3. Get lxml by running `pip install lxml` (More info [here](http://lxml.de/installation.html#where-to-get-it))
4. Get requests by running `pip install requests` (More info [here](http://docs.python-requests.org/en/master/user/install/))
5. Clone this repository or download its ZIP.

## Usage

Run main.py or use `python3 main.py` to run the script.

Commands:

* `help`
* `custom`
* `make cbz`
* `exit`/ `quit`

### `help`

Prints information on all commands and a list of already implemented comics you can download by typing the command on the left column.

### `custom`

Downloads a user-defined comic. To download a specific comic, you'll need a link to the first page, an XPath expression giving out the link to the next page and an XPath expression giving out the link to the image. More info [here](http://www.w3schools.com/xml/xpath_syntax.asp).

### `make cbz`

Creates a .cbz file using the specified folder containing the comic's images. Note: This folder must be in the same WebComicToCBZ folder for this command to work.

### `exit`/ `quit`

Leaves the command prompt.

# WebComicToCBZ

[![Build Status](https://travis-ci.org/J-CPelletier/WebComicToCBZ.svg?branch=master)](https://travis-ci.org/J-CPelletier/WebComicToCBZ)

## Description

WebComicToCBZ is a Python-based web comic downloader that can additionally create a .cbz (Comic Book ZIP) file once downloaded.

## Notice

This program is for personal use only. Please be aware that by making the downloaded comics publically available without the permission of the author, you may be infringing upon various copyrights.

## Installation

### Dependencies

* Python3
* lxml
* requests

### Process

#### With the requirements.txt

1. Install [Python 3](https://www.python.org/downloads/)
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3. Clone this repository and open a terminal in its directory.
4. Get the required packages by running `pip install -r requirements.txt`

#### Without the requirements.txt

1. Install [Python 3](https://www.python.org/downloads/)
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3. Get lxml by running `pip install lxml` (More info [here](http://lxml.de/installation.html#where-to-get-it))
4. Get requests by running `pip install requests` (More info [here](http://docs.python-requests.org/en/master/user/install/))
5. Clone this repository or download its ZIP.

## Usage

Run main.py or use `python3 main.py` to run the script.

### Commands

* `help`
* `custom`
* `make cbz`
* `exit`/ `quit`

#### `help`

Prints information on all commands and a list of already implemented comics you can download by typing the command on the left side.

#### `custom`

Downloads a user-defined comic. To download a specific comic, you'll need a link to the first page, an XPath expression giving out the link to the next page and an XPath expression giving out the link to the image. More info [here](http://www.w3schools.com/xml/xpath_syntax.asp).

#### `make cbz`

Creates a .cbz file using the specified folder containing the comic's images. Note: This folder must be in the same WebComicToCBZ folder for this command to work.

#### `exit`/ `quit`

Leaves the command prompt.

## Contribution

The procedure depends on the type of contribution:

* If you simply want to request the addition of a comic to the list of supported comics, make an issue with the label "Enhancement".
* If you want to request the addition of a feature to the system or a bugfix, make an issue with the appropriate label.

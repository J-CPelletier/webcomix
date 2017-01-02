# WebComicToCBZ

## Introduction

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

Commands:

* `help`
* `exit`/ `quit`
* `custom`

### `help`

Prints information on all commands and a list of already implemented comics you can download by typing the command on the left column.

### `exit`/ `quit`

Leaves the command prompt.

### `custom`

Downloads a user-defined comic. To download a specific comic, you'll need a link to the first page, an XPath expression giving out the link to the next page and an XPath expression giving out the link to the image.

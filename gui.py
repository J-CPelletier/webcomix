#! python3
# -*- coding: utf-8 -*-

import sys
from main import supported_comics
from comic import Comic
from PyQt5.QtWidgets import (QWidget, QLabel, 
                             QComboBox, QApplication,
                             QPushButton, QTextEdit,
                             QCheckBox, QLineEdit)

import click

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.url_defined_comic = QLabel("WebComicToCBZ", self)

        comic_list = QComboBox(self)
        for name in list(supported_comics.keys()):
            comic_list.addItem(name)

        self.make_cbz_checkbox = QCheckBox("Make a .cbz file", self)

        download_button = QPushButton("Download", self)
        download_button.clicked.connect(lambda: self.download(str(comic_list.currentText()), self.make_cbz_checkbox.isChecked()))

        self.dialog_box = QTextEdit(self)
        self.dialog_box.setReadOnly(True)

        self.name = QLineEdit(self)
        self.url = QLineEdit(self)
        self.next_page_xpath = QLineEdit(self)
        self.image_xpath = QLineEdit(self)
        self.name_label = QLabel("Name of the comic:", self)
        self.url_label = QLabel("First page URL:", self)
        self.next_page_xpath_label = QLabel("Next page XPath:", self)
        self.image_xpath_label = QLabel("Comic Image XPath:", self)

        comic_list.move(50, 50)
        download_button.move(50, 80)
        self.url_defined_comic.move(50, 150)
        self.dialog_box.move(50, 180)
        self.make_cbz_checkbox.move(50, 110)

        self.name_label.move(350, 50)
        self.name.move(475, 45)
        self.url_label.move(350, 80)
        self.url.move(475, 75)
        self.next_page_xpath_label.move(350, 110)
        self.next_page_xpath.move(475, 105)
        self.image_xpath_label.move(350, 140)
        self.image_xpath.move(475, 135)

        custom_button = QPushButton("Download", self)
        custom_button.clicked.connect(lambda: self.custom)

        comic_list.activated[str].connect(self.onActivated)

        self.setFixedSize(700, 400)
        self.setWindowTitle('WebComicToCBZ')
        self.show()


    def onActivated(self, text):
        text = supported_comics[text][0]
        self.url_defined_comic.setText(text)
        self.url_defined_comic.adjustSize()

    def download(self, name, make_cbz):
        comic = Comic(*supported_comics[name])
        comic.download(name)
        if make_cbz:
            Comic.make_cbz(name, name)

    def custom:
        pass

def show_on_console(message):
    """
    Displays usual message on GUI instead of console
    """
    ex.dialog_box.append(str(message) + "n")
    QApplication.processEvents()

click.echo = show_on_console

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

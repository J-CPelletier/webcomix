#! python3
# -*- coding: utf-8 -*-

import sys
from main import supported_comics
from comic import Comic
from PyQt5.QtWidgets import (QWidget, QLabel, 
                             QComboBox, QApplication,
                             QPushButton, QTextEdit,
                             QCheckBox)

import click

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.lbl = QLabel("WebComicToCBZ", self)

        comic_list = QComboBox(self)
        for name in list(supported_comics.keys()):
            comic_list.addItem(name)

        self.make_cbz_checkbox = QCheckBox("Make a .cbz file", self)

        download_button = QPushButton("Download", self)
        download_button.clicked.connect(lambda: self.download(str(comic_list.currentText()), self.make_cbz_checkbox.isChecked()))

        self.dialog_box = QTextEdit(self)
        self.dialog_box.setReadOnly(True)

        comic_list.move(50, 50)
        download_button.move(50, 80)
        self.lbl.move(50, 150)
        self.dialog_box.move(50, 180)
        self.make_cbz_checkbox.move(50, 110)

        comic_list.activated[str].connect(self.onActivated)

        self.setFixedSize(700, 400)
        self.setWindowTitle('WebComicToCBZ')
        self.show()


    def onActivated(self, text):
        text =  supported_comics[text][0]
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def download(self, name, make_cbz):
        comic = Comic(*supported_comics[name])
        comic.download(name)

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

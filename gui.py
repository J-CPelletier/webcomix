#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from main import supported_comics
from comic import Comic
from PyQt5.QtWidgets import (QWidget, QLabel, 
                             QComboBox, QApplication, QPushButton)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.lbl = QLabel("WebComicToCBZ", self)

        comic_list = QComboBox(self)
        for name in list(supported_comics.keys()):
            comic_list.addItem(name)

        download_button = QPushButton("Download", self)
        download_button.clicked.connect(lambda: self.download(str(comic_list.currentText())))

        comic_list.move(50, 50)
        download_button.move(50, 80)
        self.lbl.move(50, 150)

        comic_list.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('WebComicToCBZ')
        self.show()


    def onActivated(self, text):
        text =  supported_comics[text][0]
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def download(self, name):
        comic = Comic(*supported_comics[name])
        comic.download(name)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

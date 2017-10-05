#! python3
# -*- coding: utf-8 -*-

import sys

import click
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QTextEdit,
                             QWidget)

from webcomictocbz.comic import Comic
from webcomictocbz.custom_download import CustomDownload
from webcomictocbz.supported_comics import supported_comics
from webcomictocbz.supported_download import SupportedDownload


class GUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.make_cbz_checkbox = QCheckBox("Make a .cbz file", self)

        self.supported_download = SupportedDownload(self)
        self.custom_download = CustomDownload(self)

        self.dialog_box = QTextEdit(self)
        self.dialog_box.setReadOnly(True)

        self.dialog_box.move(50, 180)
        self.make_cbz_checkbox.move(275, 20)

        self.setFixedSize(700, 400)
        self.setWindowTitle('WebComicToCBZ')
        self.show()

    def closeEvent(self, event):
        sys.exit(0)

def show_on_console(message):
    """
    Displays usual message on GUI instead of console
    """
    gui.dialog_box.append(str(message))
    QApplication.processEvents()

if __name__ == '__main__':
    click.echo = show_on_console
    app = QApplication(sys.argv)
    gui = GUI()
    app.exec_()

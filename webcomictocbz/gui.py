#! python3
# -*- coding: utf-8 -*-

import sys
from .supported_comics import supported_comics
from .comic import Comic
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication,
                             QPushButton, QTextEdit,
                             QCheckBox, QLineEdit,
                             QMessageBox)

import click
from .supported_download import SupportedDownload
from .custom_download import CustomDownload

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

from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QTextEdit,
                             QWidget)

from webcomictocbz.supported_comics import supported_comics


class SupportedDownload:
    def __init__(self, parent):
        self.url_defined_comic = QLabel("WebComicToCBZ", parent)

        comic_list = QComboBox(parent)
        for name in sorted(supported_comics):
            comic_list.addItem(name)

        download_button = QPushButton("Download", parent)
        download_button.clicked.connect(lambda: self.download(str(comic_list.currentText()), parent.make_cbz_checkbox.isChecked()))

        comic_list.move(50, 50)
        download_button.move(50, 80)
        self.url_defined_comic.move(50, 150)

        comic_list.activated[str].connect(self.change_url_text)

    def change_url_text(self, text):
        text = supported_comics[text][0]
        self.url_defined_comic.setText(text)
        self.url_defined_comic.adjustSize()

    def download(self, name, make_cbz):
        comic = Comic(*supported_comics[name])
        comic.download(name)
        if make_cbz:
            Comic.make_cbz(name, name)

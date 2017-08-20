from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication,
                             QPushButton, QTextEdit,
                             QCheckBox, QLineEdit,
                             QMessageBox)
from .search import search
from .comic import Comic

class CustomDownload:
    def __init__(self, parent):
        self.name = QLineEdit(parent)
        self.url = QLineEdit(parent)
        self.next_page_xpath = QLineEdit(parent)
        self.image_xpath = QLineEdit(parent)
        self.name_label = QLabel("Name of the comic:", parent)
        self.url_label = QLabel("First page URL:", parent)
        self.next_page_xpath_label = QLabel("Next page XPath:", parent)
        self.image_xpath_label = QLabel("Comic Image XPath:", parent)
        self.discovery_button = QCheckBox("Discovery mode", parent)
        self.discovery_mode = True

        self.discovery_button.stateChanged.connect(lambda: self.set_discovery_mode())
        self.discovery_button.setChecked(True)

        custom_button = QPushButton("Download", parent)
        custom_button.clicked.connect(lambda: self.custom(self.name.text(), self.url.text(), self.next_page_xpath.text(), self.image_xpath.text(), parent.make_cbz_checkbox.isChecked()))

        self.name_label.move(350, 50)
        self.name.move(475, 45)
        self.url_label.move(350, 80)
        self.url.move(475, 75)
        self.next_page_xpath_label.move(350, 110)
        self.next_page_xpath.move(475, 105)
        self.image_xpath_label.move(350, 140)
        self.image_xpath.move(475, 135)
        self.discovery_button.move(350, 170)

        custom_button.move(500, 170)

    def custom(self, comic_name, first_page_url, next_page_xpath, image_xpath, make_cbz):
        validation = None
        if self.discovery_mode:
            comic = discovery(first_page_url)
            validation = Comic.verify_xpath(comic.url, comic.next_page_selector, comic.comic_image_selector)
            next_page_xpath, image_xpath = comic.next_page_selector, comic.comic_image_selector
        else:
            validation = Comic.verify_xpath(first_page_url, next_page_xpath, image_xpath)

        confirmation = QMessageBox()
        message = "".join(["Page {}: \nPage URL: {}\nImage URL: {}\n".format(i+1, validation[i][0], validation[i][1]) for i in range(3)])
        confirmation.setText(message)
        confirmation.setInformativeText("Verify that the links above are correct before proceeding.")
        confirmation.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirmation.buttonClicked.connect(lambda: self.custom_download(comic_name, first_page_url, next_page_xpath, image_xpath, make_cbz))
        confirmation.setWindowTitle("Confirmation")
        confirmation.exec_()

    def custom_download(self, comic_name, first_page_url, next_page_xpath, image_xpath, make_cbz):
        comic = Comic(first_page_url, next_page_xpath, image_xpath)
        comic.download(comic_name)
        if make_cbz:
            Comic.make_cbz(comic_name, comic_name)

    def set_discovery_mode(self):
        if self.discovery_button.isChecked():
            self.next_page_xpath_label.hide()
            self.next_page_xpath.hide()
            self.image_xpath.hide()
            self.image_xpath_label.hide()
            self.discovery_mode = True
        else:
            self.next_page_xpath_label.show()
            self.next_page_xpath.show()
            self.image_xpath.show()
            self.image_xpath_label.show()
            self.discovery_mode = False

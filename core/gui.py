from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QListWidget
import sys
from uztracker_scraper import scrape_uztracker
from uztracker_scraper import get_magnet_link
# from downloading.download import run_aria2p


class MainWindow(QtWidgets.QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        searchresults = []

        self.setWindowTitle("Software Manager")
        self.setGeometry(100, 100, 800, 600)

        self.controls = QWidget()
        self.controlsLayout = QVBoxLayout()

        # Widgets
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search for software...")
        self.searchbar.setClearButtonEnabled(True)
        self.searchbar.setMinimumHeight(30)
        self.searchbar.returnPressed.connect(self.return_pressed)

        self.button = QtWidgets.QPushButton("Download")
        self.softwareList = QListWidget()

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        
        containerLayout.addWidget(self.softwareList)
        self.softwareList.addItems(searchresults)

        containerLayout.addWidget(self.button)
        self.button.clicked.connect(lambda: self.download_selected())
        self.button.clicked.connect(lambda: self.get_selected_item())

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

    def download_selected(self):
        item = self.softwareList.currentItem()
        if item is not None:
            print(f"Downloading {self.softwareList.currentItem().text()}")
        else:
            print("No item selected for download.")


    def get_selected_item(self):
        item = self.softwareList.currentItem()
        if item is not None:
            return item.text()
        return ""

    def return_pressed(self):
        search_text = self.searchbar.text()
        self.postnames, self.postlinks = scrape_uztracker(search_text)
        self.softwareList.clear()
        if self.postnames:
            self.softwareList.addItems(self.postnames)
        print("User searched for:", search_text)




def run_gui():
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()

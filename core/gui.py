from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QListWidget
import sys
from uztracker_scraper import scrape_uztracker
from uztracker_scraper import get_magnet_link
from downloading.download import start_client
from downloading.download import add_magnet


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
        self.button.clicked.connect(lambda: get_item_index(self.softwareList.currentItem().text(), self.postnames, self.postlinks))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

    def return_pressed(self):
        search_text = self.searchbar.text()
        self.postnames, self.postlinks = scrape_uztracker(search_text)
        self.softwareList.clear()
        if self.postnames:
            self.softwareList.addItems(self.postnames)
        print("User searched for:", search_text)

    

def get_item_index(item, list, listlinks):
    position = list.index(item)
    if 0 <= position < len(listlinks): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
        selected = "https://uztracker.net/" + listlinks[position].lstrip("./")
        post_url = selected
        print(selected)
        selected_magnet = get_magnet_link(selected)
        add_magnet(selected_magnet)




def run_gui():
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    start_client()
    run_gui()

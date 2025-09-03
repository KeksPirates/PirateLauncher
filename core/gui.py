from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QListWidget, QToolBar
from PySide6.QtGui import QIcon, QAction
import sys
import darkdetect
from core.uztracker_scraper import scrape_uztracker
from core.uztracker_scraper import get_magnet_link
from core.downloading.download import start_client
from core.downloading.download import add_magnet


class MainWindow(QtWidgets.QMainWindow, QWidget):
    def __init__(self):
        global settings_action
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

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setLayoutDirection(Qt.RightToLeft)
        
        if darkdetect.isDark():
            settings_action = QAction(QIcon("core/assets/settings_dark.png"), "Settings", self)
        else:
            settings_action = QAction(QIcon("core/assets/settings.png"), "Settings", self)

        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)

        toolbar.setMovable(False)

    def open_settings(self):
        print("Settings clicked")

    

    def download_selected(self):
        item = self.softwareList.currentItem()
        if item is not None:
            print(f"Downloading {self.softwareList.currentItem().text()}")
            self.get_item_index(self.softwareList.currentItem().text(), self.postnames, self.postlinks)
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


    def get_item_index(self, item, list, listlinks):
        position = list.index(item)
        if 0 <= position < len(listlinks): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
            selected = "https://uztracker.net/" + listlinks[position].lstrip("./")
            post_url = selected
            print(selected)
            selected_magnet = get_magnet_link(selected)
            start_client()
            add_magnet(selected_magnet)

def run_gui():
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()

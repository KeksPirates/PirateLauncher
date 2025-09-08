from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget, QVBoxLayout, QListWidget, QToolBar, QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QIcon, QAction
import darkdetect
import requests
from core.scraping.uztracker_scraper import scrape_uztracker
from core.scraping.uztracker_scraper import get_magnet_link
from core.downloading.download import start_client
from core.downloading.download import add_magnet

def state_debug(setting):
    global debug
    if setting is True:
        debug = True
    else:
        debug = False

def choose_tracker():
    global rutracker
    choice = input("use rutracker? (y/n): ")
    print(choice)
    if choice.lower() == 'y':
        print("Using rutracker...")
        rutracker = True
    else:
        print("Using uztracker...")
        rutracker = False


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
        self.searchbar.returnPressed.connect(self.return_pressed) # Triggers scraping functions on enter
        self.button = QtWidgets.QPushButton("Download")
        self.softwareList = QListWidget()

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        
        containerLayout.addWidget(self.softwareList)
        self.softwareList.addItems(searchresults)

        containerLayout.addWidget(self.button)
        # download button triggers
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

        settings_action.triggered.connect(self.settings_dialog)
        toolbar.addAction(settings_action)

        toolbar.setMovable(False)

    def settings_dialog(self):
        if debug:
            print("Settings dialog opened")
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setFixedSize(400, 300)


        dialog.setLayout(QVBoxLayout())
        label = QLabel("This is a settings dialog.")
        QtWidgets.QPushButton("Close", clicked=dialog.close)
        # close button
        dialog.layout().addWidget(label)
        dialog.layout().addWidget(QtWidgets.QPushButton("Close", clicked=dialog.close))

        layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(dialog.reject)
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)

        self.setLayout(QVBoxLayout())
        dialog.layout().addLayout(layout)

        
        dialog.exec()

    def save_settings(self):
        pass


    def download_selected(self):
        item = self.softwareList.currentItem()
        if rutracker == True:
            if item is not None:
                if debug:
                    print(f"Downloading {self.softwareList.currentItem().text()}")
                self.get_item_index(self.softwareList.currentItem().text(), self.postnames_rutracker, self.postlinks_rutracker, debug)
            else:
                if debug:
                    print("No item selected for download.")
        else:
            if item is not None:
                if debug:
                    print(f"Downloading {self.softwareList.currentItem().text()}")
                self.get_item_index(self.softwareList.currentItem().text(), self.postnames_uztracker, self.postlinks_uztracker, debug)
            else:
                    if debug:
                        print("No item selected for download.")
            # add gui notification for no item selected


    def get_selected_item(self):
        item = self.softwareList.currentItem()
        if item is not None:
            return item.text()
        return ""


    def return_pressed(self):
        if rutracker == True:
            global postnames
            global postlinks
            search_text = self.searchbar.text()
            search = requests.get(f"https://pizzasucht.net/search/{search_text}")
            self.softwareList.clear()
            data = search.json()
            self.postnames_rutracker = data["titles"]
            for self.postnames_rutracker in data["titles"]:
                self.softwareList.addItem(self.postnames_rutracker)
            self.postnames_rutracker = data["titles"]
            self.postlinks_rutracker = data["links"]
        else:
            search_text = self.searchbar.text()
            if debug:
                print("User searched for:", search_text)
            
            response = scrape_uztracker(search_text, debug)
            if response:
                self.postnames_uztracker, self.postlinks_uztracker = response
                self.softwareList.clear()
                if self.postnames_uztracker:
                    self.softwareList.addItems(self.postnames_uztracker)
            elif debug:
                print(f"No Results found for \"{search_text}\"")

    def get_item_index(self, item, list, listlinks, debug):
        position = list.index(item)
        if 0 <= position < len(listlinks): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
            if rutracker == True:
                selected = listlinks[position]
            else:
                selected = "https://uztracker.net/" + listlinks[position].lstrip("./")
            if debug:
                print("Selected URL: ", selected)
            selected_magnet = get_magnet_link(selected, debug)
            start_client()
            add_magnet(selected_magnet)

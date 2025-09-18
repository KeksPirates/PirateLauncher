from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLineEdit, 
    QPushButton, 
    QWidget, 
    QVBoxLayout, 
    QListWidget, 
    QToolBar, 
    QDialog, 
    QLabel, 
    QHBoxLayout,
    QComboBox, 
    QSpinBox,
    QTabWidget,
    )
from PySide6.QtGui import QIcon, QAction
import darkdetect
import threading
from core.scraping.uztracker_scraper import scrape_uztracker
from core.scraping.rutracker_scraper import scrape_rutracker
from core.scraping.utils import get_magnet_link
from core.downloading.download import start_client
from core.downloading.download import add_magnet
from core.downloading.aria2p_server import set_threads



def state_debug(setting):
    global debug
    if setting is True:
        debug = True
    else:
        debug = False


def pass_aria(aria):
    global aria2process
    aria2process = aria



global tracker
tracker = "rutracker" # default tracker



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
        

        self.searchbar.returnPressed.connect(lambda: self.run_thread(threading.Thread(target=self.return_pressed))) # Triggers scraping function thread on enter
        self.button = QtWidgets.QPushButton("Download")
        self.softwareList = QListWidget()

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        
        containerLayout.addWidget(self.softwareList)
        self.softwareList.addItems(searchresults)

        containerLayout.addWidget(self.button)
        # download button triggers
        self.button.clicked.connect(lambda: self.run_thread(threading.Thread(target=self.download_selected)))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.addWidget(self.searchbar)
        self.tab1_layout.addWidget(self.softwareList)
        self.tab1.setLayout(self.tab1_layout)
        self.tabs.addTab(self.tab1,"Tab 1")

        # Tab 2
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(self.searchbar)
        self.tab2_layout.addWidget(self.softwareList)
        self.tab2.setLayout(self.tab2_layout)
        self.tabs.addTab(self.tab2,"Tab 2")

        # Tab 3
        self.tab3 = QWidget()
        self.tab3_layout = QVBoxLayout()
        self.tab3_layout.addWidget(self.searchbar)
        self.tab3_layout.addWidget(self.softwareList)
        self.tab3.setLayout(self.tab3_layout)
        self.tabs.addTab(self.tab3,"Tab 3")

        containerLayout.addWidget(self.tabs)

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        
        containerLayout.addWidget(self.softwareList)
        self.softwareList.addItems(searchresults)

        containerLayout.addWidget(self.button)
        # download button triggers
        self.button.clicked.connect(lambda: self.run_thread(threading.Thread(target=self.download_selected)))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setLayoutDirection(Qt.RightToLeft)
        
        self.tracker_list = QComboBox()
        self.tracker_list.addItems(["rutracker", "uztracker"])
        self.tracker_list.activated.connect(self.set_tracker)


        if darkdetect.isDark():
            settings_action = QAction(QIcon("core/assets/settings_dark.png"), "Settings", self)
        else:
            settings_action = QAction(QIcon("core/assets/settings.png"), "Settings", self)

        settings_action.triggered.connect(self.settings_dialog)
        toolbar.addAction(settings_action)
        toolbar.addWidget(self.tracker_list)

        toolbar.setMovable(False)

    def set_tracker(self, _):
        global tracker
        tracker = self.tracker_list.currentText()

    def settings_dialog(self):

        

        if debug:
            print("Settings dialog opened")
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setFixedSize(400, 200)


        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QLabel("Settings"))

        def close_settings():
            dialog.reject()
        
        ##################
        # THREAD SETTING #
        ##################
        thread_box = QSpinBox()
        thread_box.setMinimum(1)
        thread_box.setMaximum(16)
        thread_box.setValue(4)
        

        # container for tight space
        thread_container = QWidget()
        thread_layout = QVBoxLayout()

        thread_layout.addWidget(QLabel("Threads:"))
        thread_layout.addWidget(thread_box)
        thread_container.setLayout(thread_layout)
        thread_container.setMaximumHeight(80)
        

        # Dimensions
        thread_box.setFixedWidth(90)
        thread_box.setFixedHeight(30)

        dialog.layout().addWidget(thread_container)




        # dialog.layout().addWidget(QtWidgets.QPushButton("Close", clicked=dialog.close))

        layout = QHBoxLayout() # layout for buttons

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(lambda: self.save_settings(thread_box.value(), close_settings))

    

        cancel_btn.clicked.connect(dialog.reject)
        print(thread_box.value())
        layout.addWidget(cancel_btn)
        layout.addWidget(save_btn)
        

        dialog.layout().addLayout(layout)

        
        dialog.exec()

    def restart_aria2c(self):
        import main # had to do this because of circle import :(
        import signal
        import atexit
        global aria2process
        main.kill_aria2server(aria2process)
        aria2process.wait()
        aria2process = main.run_aria2server()
        signal.signal(signal.SIGINT, main.keyboardinterrupthandler)
        atexit.unregister(main.kill_aria2server)
        atexit.register(main.kill_aria2server, aria2process)

    def save_settings(self, thread_count, close):
        set_threads(thread_count)
        self.restart_aria2c()
        close()

    def download_selected(self):
        item = self.softwareList.currentItem()
        if item is not None:
            if debug:
                print(f"Downloading {self.softwareList.currentItem().text()}")
            self.run_thread(threading.Thread(target=self.get_item_index, args=(self.softwareList.currentItem().text(), self.postnames, self.postlinks, debug)))
        else:
            if debug:
                print("No item selected for download.")
            # add gui notification for no item selected


    def return_pressed(self):
        search_text = self.searchbar.text()
        if search_text == "":
            if debug:
                print("Error: Can't search for nothing")
            return
        if debug:
            print("User searched for:", search_text)
        if tracker == "uztracker":
            response = scrape_uztracker(search_text, debug)
        if tracker == "rutracker":
            response = scrape_rutracker(search_text, debug)
        if response:
            self.postnames, self.postlinks = response
            self.softwareList.clear()
            if self.postnames:
                self.softwareList.addItems(self.postnames)
        if not response:
            print(f"No Results found for \"{search_text}\"")
        self.softwareList.addItem("No Results")

    def get_item_index(self, item, list, listlinks, debug):
        position = list.index(item)
        if 0 <= position < len(listlinks): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
            if tracker == "uztracker":
                selected = "https://uztracker.net/" + listlinks[position].lstrip("./")
            if tracker == "rutracker":                
                selected = listlinks[position]

            if debug:
                print("Selected URL: ", selected)
            selected_magnet = get_magnet_link(selected, debug)
            start_client()
            add_magnet(selected_magnet)

    def run_thread(self, thread):
            thread.start()

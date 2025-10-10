from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer
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
    QProgressBar,
    )
from PySide6.QtGui import QIcon, QAction
import darkdetect
import threading
import asyncio
from core.data.scrapers.uztracker import scrape_uztracker
from core.data.scrapers.rutracker import scrape_rutracker
from core.utils.wrappers import run_thread
from core.utils.config.settings import save_settings
from core.utils.data.state import state
from core.utils.network.jsonhandler import split_data, format_data
from core.utils.network.download import download_selected
from core.network.aria2_integration import dlprogress


def create_tab(title, searchbar, software_list, tabs):
    tab = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(searchbar)
    layout.addWidget(software_list)
    tab.setLayout(layout)
    tabs.addTab(tab, title)
    return tab

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
        self.searchbar.returnPressed.connect(lambda: run_thread(threading.Thread(target=self.return_pressed))) # Triggers data function thread on enter
        
        self.dlbutton = QtWidgets.QPushButton("Download")
        self.softwareList = QListWidget()
        self.post_author_list = QListWidget()
        self.libraryList = QListWidget()
        self.downloadList = QListWidget()
        self.emptyLibrary = QLabel("No items in library.")
        self.emptyDownload = QLabel("No items in downloads.")
        self.progressbar = QProgressBar()

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        
        containerLayout.addWidget(self.softwareList)
        containerLayout.addWidget(self.post_author_list)
        self.softwareList.addItems(searchresults)

        # download button triggers
        self.dlbutton.clicked.connect(lambda: run_thread(threading.Thread(target=download_selected, args=(self.softwareList.currentItem(), state.posts, state.post_titles))))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        # Tabs
        self.tabs = QTabWidget()

        # Tab 1
        self.searchtab = QWidget()
        self.searchtab_layout = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.softwareList, stretch=3)
        self.horizontal_layout.addWidget(self.post_author_list)
        self.searchtab_layout.addWidget(self.searchbar)
        self.searchtab_layout.addWidget(self.dlbutton)
        self.searchtab_layout.addLayout(self.horizontal_layout)
        self.searchtab.setLayout(self.searchtab_layout)
        self.tabs.addTab(self.searchtab,"Search")
        
        self.tab2 = create_tab("Library", self.emptyLibrary, self.libraryList, self.tabs)
        self.tab3 = create_tab("Downloads", self.emptyDownload, self.downloadList, self.tabs)

        containerLayout.addWidget(self.tabs)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setLayoutDirection(Qt.RightToLeft)
        
        self.tracker_list = QComboBox()
        self.tracker_list.addItems(["rutracker", "uztracker"])
        self.tracker_list.activated.connect(self.set_tracker)


        if darkdetect.isDark():
            settings_action = QAction(QIcon("core/interface/assets/settings_dark.png"), "Settings", self)
        else:
            settings_action = QAction(QIcon("core/interface/assets/settings.png"), "Settings", self)

        settings_action.triggered.connect(self.settings_dialog)
        toolbar.addAction(settings_action)
        toolbar.addWidget(self.tracker_list)

        toolbar.setMovable(False)

        self.progressbar.setValue(0)
        containerLayout.addWidget(self.progressbar)
        
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(lambda: run_thread(threading.Thread(target=self.update_progress)))
        self.progress_timer.start(1000)

    def set_tracker(self, _):
        state.tracker = self.tracker_list.currentText()

    def settings_dialog(self):

        if state.debug:
            print("Settings dialog opened")
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setFixedSize(800, 400)

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
        thread_box.setValue(state.aria2_threads)
        

        # container for tight space
        thread_container = QWidget()
        thread_layout = QHBoxLayout()

        thread_layout.addWidget(QLabel("Threads:"))
        thread_layout.addWidget(thread_box)
        thread_container.setLayout(thread_layout)
        thread_container.setMaximumHeight(80)
        

        # Dimensions
        thread_box.setFixedWidth(90)
        thread_box.setFixedHeight(30)

        dialog.layout().addWidget(thread_container)

        ##################
        # SERVER SETTING #
        ##################
        
        api_url_container = QWidget()
        api_url_layout = QHBoxLayout()

        api_url = QLineEdit()
        api_url_layout.addWidget(QLabel("API Server URL:"))
        api_url_layout.addWidget(api_url)
        api_url_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        api_url_container.setLayout(api_url_layout)
        api_url.setText(state.api_url)
        dialog.layout().addWidget(api_url_container)

        #################
        # DOWNLOAD PATH #
        #################

        download_path_container = QWidget()
        download_path_layout = QHBoxLayout()

        download_path = QLineEdit()
        download_path_layout.addWidget(QLabel("Download Path:"))
        download_path_layout.addWidget(download_path)
        download_path_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        download_path_container.setLayout(download_path_layout)
        download_path.setText(state.download_path)
        dialog.layout().addWidget(download_path_container)

        ##################
        # SPEED LIMITING #
        ##################

        speed_limit_container = QWidget()
        speed_limit_layout = QHBoxLayout()

        speed_limit_layout.addWidget(QLabel("Max Download Speed (KiB, 0 for unlimited): "))
        speed_limit = QSpinBox()
        speed_limit.setMinimum(0)
        speed_limit.setMaximum(10000000)
        speed_limit.setValue(state.speed_limit)
        speed_limit_container.setLayout(speed_limit_layout)
        speed_limit_layout.addWidget(speed_limit)
        speed_limit.setFixedWidth(180)
        speed_limit.setFixedHeight(30)
        dialog.layout().addWidget(speed_limit_container)

        ###############
        # SAVE/CANCEL #
        ###############

        layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(lambda: save_settings(thread_box.value(), close_settings, api_url.text(), download_path.text(), speed_limit.value()))
    
        cancel_btn.clicked.connect(dialog.reject)
        print(thread_box.value())
        layout.addWidget(cancel_btn)
        layout.addWidget(save_btn)

        dialog.layout().addLayout(layout)
        
        dialog.exec()



    def return_pressed(self):
        search_text = self.searchbar.text()
        if search_text == "":
            if state.debug:
                print("Error: Can't search for nothing")
            return
        if state.debug:
            print("User searched for:", search_text)
        if state.tracker == "uztracker":
            response = asyncio.run(scrape_uztracker(search_text))
        if state.tracker == "rutracker":
            response = scrape_rutracker(search_text)
        if response:
            if state.tracker == "uztracker":
                state.post_titles, state.post_urls, = response
                self.softwareList.clear()
                if state.post_titles:
                    self.softwareList.addItems(state.post_titles)
                    self.post_author_list.addItems(state.post_author)
            if state.tracker == "rutracker":
                _, state.posts, _, _ = split_data(response)
                state.post_titles, _, state.post_author = format_data(state.posts)
                self.post_author_list.clear()
                self.post_author_list.addItems(state.post_author)
                self.softwareList.clear()
                self.softwareList.addItems(state.post_titles)
        if not response:
            if state.debug:
                print(f"No Results found for \"{search_text}\"")
            self.softwareList.clear()
            self.softwareList.addItem("No Results") # replace with no results text in center
    

    def update_progress(self):
        progress = dlprogress()
        self.progressbar.setValue(progress)

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer, QModelIndex, QAbstractTableModel, Signal
from PySide6.QtWidgets import (
    QLineEdit,
    QTableView,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QToolBar,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QTabWidget,
    QProgressBar,
    QHeaderView,
    QMessageBox,
    QTableWidget,
    )

from PySide6.QtGui import QIcon, QAction, QCloseEvent, QImage, QPixmap
import darkdetect
import threading
import platform
import requests as r
import os
import subprocess
import time
import sys
import json
from core.utils.general.wrappers import run_thread
from core.utils.data.state import state
from core.utils.network.download import download_selected
from core.utils.network.update_checker import check_for_updates
from core.utils.general.shutdown import closehelper
from core.interface.utils.tabhelper import create_tab
from core.interface.utils.searchhelper import return_pressed
from core.interface.dialogs.settings import settings_dialog
from core.network.aria2_integration import dlprogress


def download_update(latest_version):
    old_filename = f"SoftwareManager-dev-{state.version.replace('-dev', '')}-windows.exe"
    new_filename = f"SoftwareManager-dev-{latest_version.replace('-dev', '')}-windows.exe"
    url = f"https://github.com/KeksPirates/SoftwareManager/releases/latest/download/SoftwareManager-dev-{latest_version.replace('-dev', '')}-windows.exe"

    print("Downloading update...")
    if os.path.exists(old_filename):
        os.remove(old_filename)
    response = r.get(url, allow_redirects=True)
    with open(new_filename, "wb") as f:
        f.write(response.content)
    if not os.path.exists(new_filename):
        raise FileNotFoundError("Executable not found")
    subprocess.Popen([new_filename], shell=True)
    time.sleep(0.5)
    sys.exit(0)


class MainWindow(QtWidgets.QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        build_info_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "build_info.json")
        if os.path.exists(build_info_path):
            with open(build_info_path, "r") as f:
                build_info = json.load(f)
                state.version = build_info.get("version")

        # Check for updates on Windows
        if state.ignore_updates is False:
            if platform.system() == "Windows":
                result = check_for_updates()
                assets, latest_version = result

                if assets:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Update Available")
                    msg.setText("A new version is available.")
                    msg.setInformativeText("Please visit the GitHub releases page to download the latest version.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Ignore)

                    response = msg.exec_()
                    if response == QMessageBox.Ok:
                        download_update(latest_version)

        self.setWindowTitle("Software Manager")
        self.setGeometry(100, 100, 800, 600)

        self.controls = QWidget()
        self.controlsLayout = QVBoxLayout()

        # Widgets
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search for software...")
        self.searchbar.setClearButtonEnabled(True)
        self.searchbar.setMinimumHeight(30)
        self.searchbar.returnPressed.connect(lambda: run_thread(threading.Thread(target=return_pressed, args=(self,)))) # Triggers data function thread on enter

        self.dlbutton = QtWidgets.QPushButton("Download")
        self.libraryList = QListWidget()

        self.emptyResults = QLabel("No Results")
        self.emptyResults.setAlignment(Qt.AlignCenter)
        self.emptyResults.hide()

        self.download_model = None
        self.downloadList = QTableView()
        self.emptyLibrary = QLabel("No items in library.")
        self.emptyDownload = QLabel("No items in downloads.")
        self.progressbar = QProgressBar()
        self.qtablewidget = QTableWidget()

        self.qtablewidget.setColumnCount(2)
        self.qtablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.qtablewidget.verticalHeader().setVisible(False)
        self.qtablewidget.setHorizontalHeaderLabels(["Post Title", "Author"])
        self.qtablewidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.qtablewidget.setAttribute(Qt.WA_TranslucentBackground)
        self.qtablewidget.viewport().setAttribute(Qt.WA_TranslucentBackground)

        header = self.qtablewidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.resizeSection(1, 500)

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.qtablewidget)

        class DownloadModel(QAbstractTableModel):
            def __init__(self):
                super().__init__()
                self.headers = ["Name", "Status", "Progress", "Speed", "Size", "Total Size"]

            def rowCount(self, parent=QModelIndex()):
                return len(state.downloads)

            def columnCount(self, parent=QModelIndex()):
                return len(self.headers)

            def headerData(self, section, orientation, role=Qt.DisplayRole):
                if role == Qt.DisplayRole and orientation == Qt.Horizontal:
                    return self.headers[section]
                return None

            def data(self, index, role=Qt.DisplayRole):
                if role == Qt.DisplayRole:
                    download = state.downloads[index.row()]
                    col = index.column()

                    if col == 0:
                        return download.name
                    elif col == 1:
                        return getattr(download, 'status', 'Downloading')
                    elif col == 2:
                        return f"{int(download.progress)}%"
                    elif col == 3:
                        return f"{download.download_speed_string()}"
                    elif col == 4:
                        pass
                    elif col == 5:
                        return f"{download.total_length_string()}"
                return None

        self.download_model = DownloadModel()
        self.downloadList.setModel(self.download_model)
        self.downloadList.horizontalHeader().setStretchLastSection(False)
        self.downloadList.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.downloadList.setSelectionBehavior(QTableView.SelectRows)
        self.downloadList.setAttribute(Qt.WA_TranslucentBackground)
        self.downloadList.viewport().setAttribute(Qt.WA_TranslucentBackground)

        # download button triggers
        self.dlbutton.clicked.connect(lambda: run_thread(threading.Thread(target=download_selected, args=(self.qtablewidget.currentItem(), state.posts, state.post_titles))))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        # Tabs
        self.tabs = QTabWidget()

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.emptyResults, stretch=3)
        self.horizontal_layout.addWidget(self.qtablewidget)

        self.tab1 = create_tab("Search", self.searchbar, self.qtablewidget, self.tabs, self.dlbutton, self.horizontal_layout)
        self.tab2 = create_tab("Library", self.emptyLibrary, self.libraryList, self.tabs, None, None)
        self.tab3 = create_tab("Downloads", self.emptyDownload, self.downloadList, self.tabs, None, None)

        self.image = QImage(state.image_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.overlay_label = QLabel(self)
        self.overlay_label.setPixmap(self.pixmap)
        self.overlay_label.adjustSize()
        self.overlay_label.raise_()

        offset_x = -1350
        offset_y = -550
        x = self.width() - self.overlay_label.width() - offset_x
        y = self.height() - self.overlay_label.height() - offset_y
        self.overlay_label.move(x, y)

        # temporarily disabled
        # state.image_changed.connect(self.update_image_overlay)

        containerLayout.addWidget(self.tabs)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setLayoutDirection(Qt.RightToLeft)

        self.tracker_list = QComboBox()
        self.tracker_list.addItems(["rutracker", "uztracker", "m0nkrus"])
        self.tracker_list.activated.connect(self.set_tracker)

        if darkdetect.isDark():
            settings_action = QAction(QIcon("core/interface/assets/settings_white.png"), "Settings", self)
            settings_action = QAction(QIcon("core/interface/assets/settings_black.png"), "Settings", self)

        settings_action.triggered.connect(lambda: settings_dialog(self))
        toolbar.addAction(settings_action)
        toolbar.addWidget(self.tracker_list)

        toolbar.setMovable(False)

        self.progressbar.setValue(0)
        containerLayout.addWidget(self.progressbar)

        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(lambda: run_thread(threading.Thread(target=self.update_progress)))
        self.progress_timer.start(1000)

        self.download_timer = QTimer()
        self.download_timer.timeout.connect(lambda: run_thread(threading.Thread(target=self.download_list_update)))
        self.download_timer.start(500)

    def update_image_overlay(self, new_image_path):
        self.image = QImage(new_image_path)
        self.pixmap = QPixmap.fromImage(self.image)

        self.overlay_label.setPixmap(self.pixmap)
        self.overlay_label.adjustSize()

    def download_list_update(self):
        if self.download_model:
            self.download_model.layoutAboutToBeChanged.emit()
            self.download_model.layoutChanged.emit()

    def closeEvent(self, event: QCloseEvent):
        closehelper()
        event.accept()

    def set_tracker(self, _):
        state.tracker = self.tracker_list.currentText()

    def update_progress(self):
        progress = dlprogress()
        self.progressbar.setValue(progress)

    def show_empty_results(self, show: bool):
        if show:
            self.qtablewidget.hide()
            self.emptyResults.show()
        else:
            self.emptyResults.hide()
            self.qtablewidget.show()

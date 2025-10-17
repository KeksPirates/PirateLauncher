from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer, QModelIndex, QAbstractTableModel
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
    )
from PySide6.QtGui import QIcon, QAction, QCloseEvent
import darkdetect
import threading
from core.utils.general.wrappers import run_thread
from core.utils.data.state import state
from core.utils.network.download import download_selected
from core.utils.general.shutdown import closehelper
from core.interface.utils.tabhelper import create_tab
from core.interface.utils.searchhelper import return_pressed
from core.interface.dialogs.settings import settings_dialog
from core.network.aria2_integration import dlprogress



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
        self.searchbar.returnPressed.connect(lambda: run_thread(threading.Thread(target=return_pressed, args=(self,)))) # Triggers data function thread on enter
        
        self.dlbutton = QtWidgets.QPushButton("Download")
        self.softwareList = QListWidget()
        self.post_author_list = QListWidget()
        self.libraryList = QListWidget()

        self.emptyResults = QLabel("No Results")
        self.emptyResults.setAlignment(Qt.AlignCenter)
        self.emptyResults.hide()


        self.download_model = None
        self.downloadList = QTableView()
        self.emptyLibrary = QLabel("No items in library.")
        self.emptyDownload = QLabel("No items in downloads.")
        self.progressbar = QProgressBar()

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        
        containerLayout.addWidget(self.softwareList)
        containerLayout.addWidget(self.post_author_list)
        self.softwareList.addItems(searchresults)

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

        # download button triggers
        self.dlbutton.clicked.connect(lambda: run_thread(threading.Thread(target=download_selected, args=(self.softwareList.currentItem(), state.posts, state.post_titles))))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        # Tabs
        self.tabs = QTabWidget()

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.softwareList, stretch=3)
        self.horizontal_layout.addWidget(self.emptyResults, stretch=3)
        self.horizontal_layout.addWidget(self.post_author_list)
        
        self.tab1 = create_tab("Search", self.searchbar, self.softwareList, self.tabs, self.dlbutton, self.horizontal_layout)
        self.tab2 = create_tab("Library", self.emptyLibrary, self.libraryList, self.tabs, None, None)
        self.tab3 = create_tab("Downloads", self.emptyDownload, self.downloadList, self.tabs, None, None)

        containerLayout.addWidget(self.tabs)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setLayoutDirection(Qt.RightToLeft)
        
        self.tracker_list = QComboBox()
        self.tracker_list.addItems(["rutracker", "uztracker", "m0nkrus"])
        self.tracker_list.activated.connect(self.set_tracker)


        if darkdetect.isDark():
            settings_action = QAction(QIcon("core/interface/assets/settings_dark.png"), "Settings", self)
        else:
            settings_action = QAction(QIcon("core/interface/assets/settings.png"), "Settings", self)

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
            self.softwareList.hide()
            self.emptyResults.show()
        else:
            self.emptyResults.hide()
            self.softwareList.show()

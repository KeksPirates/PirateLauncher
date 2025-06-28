from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLayoutItem, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
import sys

class MainWindow(QtWidgets.QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
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
        self.softwareList.addItems(["Software A", "Software B", "Software C", "Software D"])

        containerLayout.addWidget(self.button)
        self.button.clicked.connect(lambda: print(f"Downloading {self.softwareList.currentItem().text()}"))

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        containerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

    def return_pressed(self):
        search_text = self.searchbar.text()
        print("User searched for:", search_text)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())

from core.utils.config.settings import save_settings
from core.utils.data.state import state
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QLineEdit, 
    QPushButton, 
    QWidget, 
    QVBoxLayout, 
    QDialog, 
    QLabel, 
    QHBoxLayout,
    QSpinBox,
    )





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
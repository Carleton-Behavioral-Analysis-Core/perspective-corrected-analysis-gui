import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidget, QMessageBox
from behavior_analysis_tool.widgets import *
from pathlib import Path
import pandas as pd
import logging

class LoadVideosTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.logger = logging.getLogger(__name__)

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title = QLabel('Load Videos')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        
        self.video_folder_widget = MaterialFolderBrowseEdit("VIDEO FOLDER")
        layout.addWidget(self.video_folder_widget)
        
        self.dlc_folder_widget = MaterialFolderBrowseEdit("DEEPLABCUT FOLDER")
        layout.addWidget(self.dlc_folder_widget)

        self.create_project_button = MaterialPushButton("LOAD FILES")
        self.create_project_button.clicked.connect(self.update_files)
        layout.addWidget(self.create_project_button)

        layout.addSpacing(32)
        files_widget = QWidget()
        files_widget_layout = EmptyQHBoxLayout()

        video_column = EmptyQVBoxLayout()
        video_column_label = MaterialLabel("VIDEO")
        video_column_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        video_column.addWidget(video_column_label)
        self.video_list_widget = QListWidget()
        video_column.addWidget(self.video_list_widget)

        dlc_column = EmptyQVBoxLayout()
        dlc_column_label = MaterialLabel("DLC FILE")
        dlc_column_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        dlc_column.addWidget(dlc_column_label)
        self.dlc_list_widget = QListWidget()
        dlc_column.addWidget(self.dlc_list_widget)

        files_widget_layout.addLayout(video_column)
        files_widget_layout.addLayout(dlc_column)
        
        files_widget.setLayout(files_widget_layout)
        layout.addWidget(files_widget)
        self.setLayout(layout)

        self.model.config_changed_signal.connect(self.model_config_changed)

    def update_files(self):
        video_folder = self.video_folder_widget.line_edit.text()
        dlc_folder = self.dlc_folder_widget.line_edit.text()
       
        if os.path.exists(video_folder) and video_folder != "..." and os.path.exists(dlc_folder) and dlc_folder != "..." and self.model.config_path != None:
            self.model.load_videos_and_dlc_files(video_folder, dlc_folder)
        elif self.model.config_path == None:
            logger.warn("No Path to Config File Found")
        elif not os.path.exists(video_folder) or video_folder == "...":
            logger.warn("No Path to Video Folder Found")
        elif not os.path.exists(dlc_folder) or dlc_folder == "...":
            logger.warn("No Path to DLC Video Folder Found")
        

    def model_config_changed(self):
        video_folder_path = self.model.config.get('video_folder_path', 'n/a')
        self.video_folder_widget.line_edit.setText(str(video_folder_path))

        dlc_folder_path = self.model.config.get('dlc_folder_path', 'n/a')
        self.dlc_folder_widget.line_edit.setText(str(dlc_folder_path))

        self.dlc_list_widget.clear()
        self.video_list_widget.clear()
        for video in self.model.config['video_data']:
            video_data = self.model.config['video_data'][video]
            self.video_list_widget.addItem(video)
            self.dlc_list_widget.addItem(video_data['dlc_file'])

    
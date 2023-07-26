from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidget, QMessageBox
from ui_design.widgets import *
from pathlib import Path
import pandas as pd

class LoadVideosTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        
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

    def update_files(self):
        video_folder = self.video_folder_widget.line_edit.text()
        dlc_folder = self.dlc_folder_widget.line_edit.text()
        # TODO exception if folders don't exist

        video_folder = Path(video_folder)
        dlc_folder = Path(dlc_folder)
        videos = (
            list(video_folder.glob('*.mp4')) + 
            list(video_folder.glob('*.MP4'))
        )
        # TODO exception if no videos were found
        data = []
        for video in videos:
            fname, _ = video.parts[-1].split('.')
            dlc_file = next(dlc_folder.glob(f"{fname}DLC*.h5"))
            # TODO exception if can't find matching DLC file
            data.append({'video': video.parts[-1], 'dlc_file': dlc_file.parts[-1]})

        # Store data for later usage
        self.df = pd.DataFrame(data)

        # Update display
        self.dlc_list_widget.clear()
        self.video_list_widget.clear()
        for idx, row in self.df.iterrows():
            self.video_list_widget.addItem(row.video)
            self.dlc_list_widget.addItem(row.dlc_file)

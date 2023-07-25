from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidget
from ui_design.widgets import MaterialLineEdit, MaterialFileBrowseEdit, EmptyQHBoxLayout, EmptyQVBoxLayout, MaterialLabel

class LoadVideosTab(QWidget):
    def __init__(self, label_column_width=50, button_column_width=100):
        super().__init__()
        self.button_column_width = button_column_width
        self.label_column_width = label_column_width
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        title = QLabel('Load Videos')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        
        self.video_folder_widget = MaterialFileBrowseEdit("VIDEO FOLDER")
        layout.addWidget(self.video_folder_widget)
        
        self.dlc_folder_widget = MaterialFileBrowseEdit("DEEPLABCUT FOLDER")
        layout.addWidget(self.dlc_folder_widget)

        self.create_project_button = QPushButton("LOAD FILES")
        self.create_project_button.setProperty('class', 'material-button')
        self.create_project_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.create_project_button)

        layout.addSpacing(32)
        files_widget = QWidget()
        files_widget_layout = EmptyQHBoxLayout()

        video_column = EmptyQVBoxLayout()
        video_column.addWidget(MaterialLabel("VIDEO"))
        video_column.addWidget(QListWidget())

        dlc_column = EmptyQVBoxLayout()
        dlc_column.addWidget(MaterialLabel("DLC FILE"))
        dlc_column.addWidget(QListWidget())

        files_widget_layout.addLayout(video_column)
        files_widget_layout.addLayout(dlc_column)
        
        files_widget.setLayout(files_widget_layout)
        layout.addWidget(files_widget)
        self.setLayout(layout)

    
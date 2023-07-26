from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import *

class LoadProjectTab(QWidget):
    def __init__(self, label_column_width=50, button_column_width=100):
        super().__init__()
        self.button_column_width = button_column_width
        self.label_column_width = label_column_width
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title = QLabel('Load Existing Project')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)

        self.project_folder_widget = MaterialFileBrowseEdit("CONFIG FILE")
        layout.addWidget(self.project_folder_widget)
        
        self.load_project_button = MaterialPushButton("LOAD PROJECT")
        self.load_project_button.setProperty('class', 'material-button')
        self.load_project_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.load_project_button)
        self.setLayout(layout)
    
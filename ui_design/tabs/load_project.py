from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import *

class LoadProjectTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        
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
    
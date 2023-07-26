from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import *

class CreateProjectTab(QWidget):
    def __init__(self, label_column_width=50, button_column_width=100):
        super().__init__()
        self.button_column_width = button_column_width
        self.label_column_width = label_column_width
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title = QLabel('Create New Project')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        self.project_name_widget = MaterialLineEdit("NAME")
        layout.addWidget(self.project_name_widget)
        self.project_folder_widget = MaterialFolderBrowseEdit("FOLDER")
        layout.addWidget(self.project_folder_widget)
        self.create_project_button = MaterialPushButton("CREATE PROJECT")
        self.create_project_button.setProperty('class', 'material-button')
        self.create_project_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.create_project_button)
        self.setLayout(layout)

    
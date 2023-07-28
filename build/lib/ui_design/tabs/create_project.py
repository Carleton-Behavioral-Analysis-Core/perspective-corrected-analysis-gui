from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import *

class CreateProjectTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

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
        layout.addWidget(self.create_project_button)
        self.setLayout(layout)

        self.create_project_button.clicked.connect(self.create_project)

    def create_project(self):
        name = self.project_name_widget.line_edit.text()
        folder = self.project_folder_widget.line_edit.text()
        self.model.create_project(folder, name)
        

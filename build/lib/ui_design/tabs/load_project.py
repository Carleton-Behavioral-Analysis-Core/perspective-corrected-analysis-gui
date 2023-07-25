from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import MaterialLineEdit, MaterialFileBrowseEdit

class LoadProjectTab(QWidget):
    def __init__(self, label_column_width=50, button_column_width=100):
        super().__init__()
        self.button_column_width = button_column_width
        self.label_column_width = label_column_width
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        title = QLabel('Load Existing Project')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)

        self.project_folder_widget = MaterialFileBrowseEdit("CONFIG FILE")
        layout.addWidget(self.project_folder_widget)
        
        self.load_project_button = QPushButton("LOAD PROJECT")
        self.load_project_button.setProperty('class', 'material-button')
        self.load_project_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.load_project_button)
        self.setLayout(layout)

    
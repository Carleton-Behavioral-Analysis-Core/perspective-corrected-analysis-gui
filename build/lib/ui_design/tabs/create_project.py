from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import MaterialLineEdit, MaterialFileBrowseEdit

class CreateProjectTab(QWidget):
    def __init__(self, label_column_width=50, button_column_width=100):
        super().__init__()
        self.button_column_width = button_column_width
        self.label_column_width = label_column_width
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        title = QLabel('Create New Project')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        self.project_name_widget = MaterialLineEdit("NAME")
        layout.addWidget(self.project_name_widget)
        self.project_folder_widget = MaterialFileBrowseEdit("FOLDER")
        layout.addWidget(self.project_folder_widget)
        self.create_project_button = QPushButton("CREATE PROJECT")
        self.create_project_button.setProperty('class', 'material-button')
        self.create_project_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.create_project_button)
        self.setLayout(layout)

    
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from ui_design.widgets import *
import logging

class LoadProjectTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.logger = logging.getLogger(__name__)

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title = QLabel('Load Existing Project')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)

        self.project_folder_widget = MaterialFolderBrowseEdit("PROJECT PATH (must contain config.yaml file)")
        layout.addWidget(self.project_folder_widget)
        
        self.load_project_button = MaterialPushButton("LOAD PROJECT")
        layout.addWidget(self.load_project_button)
        self.setLayout(layout)

        self.load_project_button.clicked.connect(self.load_project)
        self.model.config_changed_signal.connect(self.model_config_changed)

    def load_project(self):
        self.logger.info("Load project button clicked")
        self.model.load_project(self.project_folder_widget.line_edit.text())

    def model_config_changed(self):
        self.project_folder_widget.line_edit.setText(str(self.model.config_path.parent))

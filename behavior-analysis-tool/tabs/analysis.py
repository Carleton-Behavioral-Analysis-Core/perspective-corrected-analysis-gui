import numpy as np
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox
from behavior_analysis_tool.widgets import *


class AnalysisTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        title = QLabel('Analysis')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        
        hbox = EmptyQHBoxLayout()
        create_default_zones_button = MaterialPushButton("CREATE DEFAULT ZONES")
        run_analysis_button = MaterialPushButton("ANALYZE")
        hbox.addWidget(create_default_zones_button)
        hbox.addSpacing(16)
        hbox.addWidget(run_analysis_button)

        layout.addLayout(hbox)
        self.setLayout(layout)

        create_default_zones_button.clicked.connect(self.model.create_default_analysis_zones)
        run_analysis_button.clicked.connect(self.model.perform_analysis)
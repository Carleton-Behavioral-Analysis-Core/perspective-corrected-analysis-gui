import numpy as np
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox, QProgressBar
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
        self.pbar = QProgressBar(self)
        self.pbar.setVisible(False)
        hbox.addWidget(create_default_zones_button)
        hbox.addSpacing(16)
        hbox.addWidget(run_analysis_button)
        hbox.addSpacing(16)
        hbox.addWidget(self.pbar)
        layout.addLayout(hbox)
        self.setLayout(layout)

        create_default_zones_button.clicked.connect(self.model.create_default_analysis_zones)
        run_analysis_button.clicked.connect(self.preform_analysis_and_pbar)
        self.model.progressbar_changed_signal.connect(self.set_pbar_value)

    def preform_analysis_and_pbar(self):
        self.pbar.setVisible(True)
        self.set_pbar_value(0)
        self.model.perform_analysis()
        # self.set_pbar_value(100)
        

    def set_pbar_value(self, x):
        self.pbar.setValue(x)

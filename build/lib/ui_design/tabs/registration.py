import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox
from ui_design.widgets import MaterialLineEdit, MaterialFileBrowseEdit, MaterialLabel, EmptyQHBoxLayout, EmptyQVBoxLayout, MaterialLabelImage, MaterialComboBox


class RegistrationTab(QWidget):
    def __init__(self, label_column_width=50, button_column_width=100):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        title = QLabel('Register Points')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        
        sublayout = EmptyQHBoxLayout()
        layout.addLayout(sublayout)

        left_widget = QWidget()
        left_widget_layout = EmptyQVBoxLayout()
        left_widget.setLayout(left_widget_layout)
        sublayout.addWidget(left_widget)
        original_video_widget = MaterialLabelImage("ORIGINAL VIDEO (click to register points)")
        corrected_video_widget = MaterialLabelImage("REGISTRATION VALIDATION")
        left_widget_layout.addWidget(original_video_widget)
        left_widget_layout.addSpacing(16)
        left_widget_layout.addWidget(corrected_video_widget)

        sublayout.addSpacing(16)

        right_widget = QWidget()
        # right_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        right_widget_layout = EmptyQVBoxLayout()
        right_widget_layout.setAlignment(QtCore.Qt.AlignTop)
        right_widget.setLayout(right_widget_layout)
        sublayout.addWidget(right_widget)
        width_line_edit = MaterialLineEdit("WIDTH [mm]")
        height_line_edit = MaterialLineEdit("HEIGHT [mm]")
        globals_groupbox = QGroupBox("GLOBALS")
        globals_layout = EmptyQVBoxLayout()
        size_layout = EmptyQHBoxLayout()
        size_layout.addWidget(width_line_edit)
        size_layout.addSpacing(16)
        size_layout.addWidget(height_line_edit)
        globals_layout.addLayout(size_layout)
        globals_groupbox.setLayout(globals_layout)
        right_widget_layout.addWidget(globals_groupbox)

        right_widget_layout.addSpacing(24)

        registration_group_box = QGroupBox("VIDEO REGISTRATION")
        registration_group_box_layout = EmptyQVBoxLayout()
        registration_group_box.setLayout(registration_group_box_layout)
        video_combo_box = MaterialComboBox("VIDEO")
        registration_group_box_layout.addWidget(video_combo_box)
        tl_line_edit = MaterialLineEdit("TOP LEFT")
        registration_group_box_layout.addWidget(tl_line_edit)
        t2_line_edit = MaterialLineEdit("TOP RIGHT")
        registration_group_box_layout.addWidget(t2_line_edit)
        t3_line_edit = MaterialLineEdit("BOTTOM RIGHT")
        registration_group_box_layout.addWidget(t3_line_edit)
        t4_line_edit = MaterialLineEdit("BUTTOM LEFT")
        registration_group_box_layout.addWidget(t4_line_edit)
        right_widget_layout.addWidget(registration_group_box)

        right_widget_layout.addSpacing(24)

        registrations_complete_button = QPushButton("ALL VIDEOS REGISTERED")
        registrations_complete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        right_widget_layout.addWidget(registrations_complete_button)
        self.setLayout(layout)

    
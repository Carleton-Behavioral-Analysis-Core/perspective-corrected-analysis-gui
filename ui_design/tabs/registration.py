import numpy as np
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox
from ui_design.widgets import *


class RegistrationTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        title = QLabel('Register Points')
        title.setProperty('class', 'material-h1')
        layout.addWidget(title)
        
        sublayout = EmptyQHBoxLayout()
        layout.addLayout(sublayout)

        left_widget = QWidget()
        left_widget_layout = EmptyQVBoxLayout()
        left_widget.setLayout(left_widget_layout)
        sublayout.addWidget(left_widget)
        self.original_video_widget = MaterialLabelImageRegisterPoints("ORIGINAL VIDEO (click to register points)",320,480,True) 
        corrected_video_widget = MaterialLabelImage("REGISTRATION VALIDATION")
        left_widget_layout.addWidget(self.original_video_widget)
        left_widget_layout.addSpacing(16)
        left_widget_layout.addWidget(corrected_video_widget)

        sublayout.addSpacing(16)

        right_widget = QWidget()
        # right_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        right_widget_layout = EmptyQVBoxLayout()
        right_widget_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        right_widget.setLayout(right_widget_layout)
        sublayout.addWidget(right_widget)
        self.width_line_edit = MaterialLineEditWidth("WIDTH [mm]","")
        self.height_line_edit = MaterialLineEditHeight("HEIGHT [mm]","")
        save_measurments = MaterialPushButton("SAVE MEASURMENTS")
        save_measurments.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        save_measurments.clicked.connect(self.model_update_width_and_height)
        
        globals_groupbox = QGroupBox("GLOBALS")
        globals_layout = EmptyQVBoxLayout()
        size_layout = EmptyQHBoxLayout()
        size_layout.addWidget(self.width_line_edit)
        size_layout.addSpacing(16)
        size_layout.addWidget(self.height_line_edit)
        globals_layout.addLayout(size_layout)
        globals_layout.addWidget(save_measurments)
        globals_groupbox.setLayout(globals_layout)
        right_widget_layout.addWidget(globals_groupbox)

        right_widget_layout.addSpacing(24)

        registration_group_box = QGroupBox("VIDEO REGISTRATION")
        registration_group_box_layout = EmptyQVBoxLayout()
        registration_group_box.setLayout(registration_group_box_layout)
        self.video_combo_box = MaterialComboBox("VIDEO")
        registration_group_box_layout.addWidget(self.video_combo_box)
        # tl_line_edit = MaterialLineEditRegisterPoints("TOP LEFT","",self.original_video_widget ,0)
        # registration_group_box_layout.addWidget(tl_line_edit)
        # t2_line_edit = MaterialLineEditRegisterPoints("TOP RIGHT","",self.original_video_widget,1)
        # registration_group_box_layout.addWidget(t2_line_edit)
        # t3_line_edit = MaterialLineEditRegisterPoints("BOTTOM RIGHT","",self.original_video_widget,2)
        # registration_group_box_layout.addWidget(t3_line_edit)
        # t4_line_edit = MaterialLineEditRegisterPoints("BOTTOM LEFT","",self.original_video_widget,3)
        # registration_group_box_layout.addWidget(t4_line_edit)
        line_edits = RegisterPointsFieldCombined("", 320,480,self.original_video_widget)
        registration_group_box_layout.addWidget(line_edits)

        right_widget_layout.addSpacing(8)

        row = EmptyQHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        clear_points = MaterialPushButton("APPLY TO ALL VIDEOS")
        clear_points.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        row.addWidget(clear_points)
        clear_points = MaterialPushButton("CLEAR")
        clear_points.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        row.addWidget(clear_points)
        registration_group_box_layout.addLayout(row)
        right_widget_layout.addWidget(registration_group_box)

        right_widget_layout.addSpacing(24)

        row = EmptyQHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        clear_all_button = MaterialPushButton("CLEAR ALL")
        registrations_complete_button = MaterialPushButton("NEXT STEP")
        row.addWidget(clear_all_button)
        row.addWidget(registrations_complete_button)
        right_widget_layout.addLayout(row)

        self.setLayout(layout)

        self.model.config_changed_signal.connect(self.model_config_changed)

    def model_config_changed(self):
        self.width_line_edit.line_edit.setPlaceholderText(str(self.model.config['box_width']))
        self.height_line_edit.line_edit.setPlaceholderText(str(self.model.config['box_height']))
        # points = {}
        # for key in self.model.config["video_data"]:
        #     points[key] = self.model.config["video_data"]["registration_points"]
        # self.original_video_widget.points_storage = points

    def model_update_width_and_height(self):
        # try:
        if True:
            print("1")
            float(self.width_line_edit.line_edit.placeholderText())
            float(self.height_line_edit.line_edit.placeholderText())
            print("1")
            self.model.register_measurements(float(self.width_line_edit.line_edit.placeholderText()), float(self.height_line_edit.line_edit.placeholderText()))
        # except:
        #     print("exception")

class MaterialLineEditWidth(MaterialLineEdit):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__(label_text, default_line_edit)
   
        self.line_edit.returnPressed.connect(self.updateWidth)
    
    def updateWidth(self):
        num = self.line_edit.text()
        if str(num).isnumeric() and float(num) > 0:
            try:
                num = float(num)
                self.line_edit.setPlaceholderText(str(num))
                self.line_edit.setText("")
            except:
                pass
            

class MaterialLineEditHeight(MaterialLineEdit):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__(label_text, default_line_edit)
   
        self.line_edit.returnPressed.connect(self.updateHeight)
    
    def updateHeight(self):
        num = self.line_edit.text()
        if str(num).isnumeric() and float(num) > 0:
            try:
                num = float(num)
                self.line_edit.setPlaceholderText(str(num))
                self.line_edit.setText("")
            except:
                pass
            
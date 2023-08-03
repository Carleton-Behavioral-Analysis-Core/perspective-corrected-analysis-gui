import numpy as np
import logging
import matplotlib.pyplot as plt
import cv2 

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox
from behavior_analysis_tool.widgets import *
from behavior_analysis_tool.utils import *
from pathlib import Path

logger = logging.getLogger(__name__)

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
        self.original_video_widget = MaterialLabelImage("ORIGINAL VIDEO (click to register points)")
        # self.original_video_widget = MaterialLabelImageRegisterPoints("ORIGINAL VIDEO (click to register points)",320,480,True) 
        self.corrected_video_widget = MaterialLabelImage("REGISTRATION VALIDATION",320, 480,False)
        left_widget_layout.addWidget(self.original_video_widget)
        left_widget_layout.addSpacing(16)
        left_widget_layout.addWidget(self.corrected_video_widget)

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

        self.keypoint_combo_box = MaterialComboBox("KEYPOINT")
        registration_group_box_layout.addWidget(self.keypoint_combo_box)

        # tl_line_edit = MaterialLineEditRegisterPoints("TOP LEFT","",self.original_video_widget ,0)
        # registration_group_box_layout.addWidget(tl_line_edit)
        # t2_line_edit = MaterialLineEditRegisterPoints("TOP RIGHT","",self.original_video_widget,1)
        # registration_group_box_layout.addWidget(t2_line_edit)
        # t3_line_edit = MaterialLineEditRegisterPoints("BOTTOM RIGHT","",self.original_video_widget,2)
        # registration_group_box_layout.addWidget(t3_line_edit)
        # t4_line_edit = MaterialLineEditRegisterPoints("BOTTOM LEFT","",self.original_video_widget,3)
        # registration_group_box_layout.addWidget(t4_line_edit)

        vlayout = EmptyQVBoxLayout()
        self.registration_labels = [
            'top left',
            'top right',
            'bottom right',
            'bottom left'
        ]
        self.n_registration_points = len(self.registration_labels)
        self.registration_colors = (plt.get_cmap()(np.linspace(0,1,self.n_registration_points))*255).astype(int)
        self.registration_points = {"": np.zeros(shape=(self.n_registration_points, 2), dtype=int)}

        self.registration_point_line_edit_matrix = []
        for i in range(self.n_registration_points):
            self.keypoint_combo_box.combo_box.addItem(self.registration_labels[i])
            row_layout = EmptyQHBoxLayout()
            x = MaterialLineEdit(f"{self.registration_labels[i]} x")
            y = MaterialLineEdit(f"{self.registration_labels[i]} y")
            row_layout.addWidget(x)
            row_layout.addWidget(y)
            vlayout.addLayout(row_layout)
            self.registration_point_line_edit_matrix.append([x,y])
            x.line_edit.textEdited.connect(lambda _: self.update_registration_points_from_line_edit(i,0))
            y.line_edit.textEdited.connect(lambda _: self.update_registration_points_from_line_edit(i,1))

        self.keypoint_combo_box.combo_box.setCurrentIndex(0)
        registration_group_box_layout.addLayout(vlayout)
        # self.registration_line_edits = RegisterPointsFieldCombined("", 320,480,self.original_video_widget)
        # registration_group_box_layout.addWidget(self.registration_line_edits)

        right_widget_layout.addSpacing(8)

        row = EmptyQHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        # apply_to_all_videos = MaterialPushButton("APPLY TO ALL VIDEOS")
        # row.addWidget(apply_to_all_videos)
        # clear_points = MaterialPushButton("CLEAR")
        # row.addWidget(clear_points)
        registration_group_box_layout.addLayout(row)
        right_widget_layout.addWidget(registration_group_box)

        right_widget_layout.addSpacing(24)

        row = EmptyQHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        # clear_all_button = MaterialPushButton("CLEAR ALL")
        registrations_complete_button = MaterialPushButton("SAVE ALL")
        # row.addWidget(clear_all_button)
        row.addWidget(registrations_complete_button)
        registrations_complete_button.clicked.connect(self.save_registrations)
        right_widget_layout.addLayout(row)

        self.setLayout(layout)
        self.model.config_changed_signal.connect(self.model_config_changed)
        self.video_combo_box.combo_box.currentIndexChanged.connect(self.video_changed)
        self.original_video_widget.mouseclick_signal.connect(self.registration_clicked)

    def redraw_registration_points(self):
        self.original_video_widget.clean()
        video = self.video_combo_box.combo_box.currentText()

        if video != "" and video in self.registration_points:
            for i in range(len(self.registration_points[video])):
                x,y = self.registration_points[video][i]
                self.original_video_widget.add_point(x,y,color=self.registration_colors[i])
                xinput, yinput = self.registration_point_line_edit_matrix[i]
                xinput.line_edit.setText(str(x))
                yinput.line_edit.setText(str(y))

            schema = self.model.get_schema().astype(np.float32)
            registration = self.registration_points[video].astype(np.float32)
            transform = get_homography(registration, schema)
            try:
                transformed_frame = cv2.warpPerspective(
                    self.original_video_widget.base_image,
                    transform, 
                    (int(self.model.config['box_width']), int(self.model.config['box_height']))
                )
                self.corrected_video_widget.set_image(transformed_frame)
            except:
                logger.warn(f"Issue with points")

        self.original_video_widget.update()

    def update_registration_points_from_line_edit(self, i, j):
        self.keypoint_combo_box.combo_box.setCurrentIndex(0)
        video = self.video_combo_box.combo_box.currentText()

        if video != "" and video in self.registration_points:
            for k, (xinput, yinput) in enumerate(self.registration_point_line_edit_matrix):
                try:
                    x = xinput.line_edit.text()
                    y = yinput.line_edit.text()
                    if x == "" or int(x) < 0:
                        x = 0
                    if y == "" or int(y) < 0:
                        y = 0
                    self.registration_points[video][k,0] = int(x)
                    self.registration_points[video][k,1] = int(y)
                except:
                    logger.warn(f"Could not read coordinates %s, %s", xinput.line_edit.text(), yinput.line_edit.text())

        self.redraw_registration_points()

    def registration_clicked(self, x, y):
        logger.info('Registration clicked %i %i', x, y)
        keypoint_index = self.keypoint_combo_box.combo_box.currentIndex()
        video_name = self.video_combo_box.combo_box.currentText()
        self.registration_points[video_name][keypoint_index,0] = x
        self.registration_points[video_name][keypoint_index,1] = y
        self.redraw_registration_points()
        self.keypoint_combo_box.combo_box.setCurrentIndex((keypoint_index+1)%self.n_registration_points)

    def save_registrations(self):
        if self.model.config_path != None and os.path.exists(self.model.config_path) and os.path.exists(self.model.config['video_folder_path']) and os.path.exists(self.model.config['dlc_folder_path']):
            for video in self.registration_points:
                self.model.config['video_data'][video]['registration_points'] = self.registration_points[video].tolist()

            self.model.dump_config()
        elif self.model.config_path == None or not os.path.exists(self.model.config_path):
            logger.warn("No Path to Config File Found")
        elif not os.path.exists(self.model.config['video_folder_path']):
            logger.warn("No Path to Video Folder Found")
        elif not os.path.exists(self.model.config['video_folder_path']):
            logger.warn("No Path to DLC Video Folder Found")

        

    def model_config_changed(self):
        self.width_line_edit.line_edit.setText(str(self.model.config['box_width']))
        self.height_line_edit.line_edit.setText(str(self.model.config['box_height']))

        self.registration_points = {}
        self.video_combo_box.combo_box.clear()
        for video in self.model.config['video_data']:
            self.video_combo_box.combo_box.addItem(video)
            self.registration_points[video] = np.array(self.model.config['video_data'][video]['registration_points'])
            
        self.video_changed()

    def video_changed(self):
        current_video = self.video_combo_box.combo_box.currentText()
        self.keypoint_combo_box.combo_box.setCurrentIndex(0)

        if current_video:
            video_info = self.model.config['video_data']
            video_folder = Path(self.model.config['video_folder_path'])
            video_fullpath = video_folder / current_video
            logger.info("Video changed to %s", video_fullpath)
            video_reader = VideoReader(video_fullpath)
            default_frame = video_reader[len(video_reader) // 2]
            self.original_video_widget.set_image(default_frame)
            self.redraw_registration_points()

    def model_update_width_and_height(self):
        if self.model.config_path != None and os.path.exists(self.model.config_path) and os.path.exists(self.model.config['video_folder_path']) and os.path.exists(self.model.config['dlc_folder_path']):
            try:
                width = float(self.width_line_edit.line_edit.text())
                height = float(self.height_line_edit.line_edit.text())
                if width > 0 and height >0:
                    logger.info('Saving measurements w=%i h=%i', width, height)
                    self.model.register_measurements(width, height)
                else:
                    raise Exception
            except:
                logger.warn("Cannot Have Negative Measurements")
                self.width_line_edit.line_edit.setText(str(self.model.config['box_width']))
                self.height_line_edit.line_edit.setText(str(self.model.config['box_height']))
        elif self.model.config_path == None or not os.path.exists(self.model.config_path):
            logger.warn("No Path to Config File Found")
        elif not os.path.exists(self.model.config['video_folder_path']):
            logger.warn("No Path to Video Folder Found")
        elif not os.path.exists(self.model.config['video_folder_path']):
            logger.warn("No Path to DLC Video Folder Found")


class MaterialLineEditWidth(MaterialLineEdit):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__(label_text, default_line_edit)
   
    #     self.line_edit.returnPressed.connect(self.updateWidth)
    
    # def updateWidth(self):
    #     num = self.line_edit.text()
    #     if str(num).isnumeric() and float(num) > 0:
    #         try:
    #             num = float(num)
    #             self.line_edit.setPlaceholderText(str(num))
    #             self.line_edit.setText("")
    #         except:
    #             pass
            

class MaterialLineEditHeight(MaterialLineEdit):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__(label_text, default_line_edit)
   
    #     self.line_edit.returnPressed.connect(self.updateHeight)
    
    # def updateHeight(self):
    #     num = self.line_edit.text()
    #     if str(num).isnumeric() and float(num) > 0:
    #         try:
    #             num = float(num)
    #             self.line_edit.setPlaceholderText(str(num))
    #             self.line_edit.setText("")
    #         except:
    #             pass
            
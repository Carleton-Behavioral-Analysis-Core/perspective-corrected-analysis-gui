import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox
from ui_design.widgets import MaterialLineEdit, MaterialFileBrowseEdit, MaterialLabel, EmptyQHBoxLayout, EmptyQVBoxLayout, MaterialLabelImage, MaterialComboBox
from PyQt5.QtGui import QImage, QPixmap


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
        original_video_widget = MaterialLabelImageRegisterPoints("ORIGINAL VIDEO (click to register points)",320,480,True) 
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
        self.video_combo_box = MaterialComboBox("VIDEO")
        registration_group_box_layout.addWidget(self.video_combo_box)
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

class MaterialLabelImageRegisterPoints(QWidget):
    def __init__(self, label_text="", height=320, width=480,Clickable = False):
        super().__init__()

        layout = EmptyQVBoxLayout()
        self.title_label = MaterialLabel(label_text)
        layout.addWidget(self.title_label)

        self.frame_label = QLabel()
        self.height = height
        self.width = width
        placeholder_frame = np.zeros(shape=(self.height,self.width,3), dtype=np.uint8)
        self.set_image(placeholder_frame)
        if Clickable:
            """ insert config file refernce like config = openYaml()
            self.points_storage = {}
            {for i in range(len(config["video_data"])): /or for key in config["video_data"]:}
            try:
                self.points_storage[{key/config["video_data"][i][title]}] = config["video_data"][{key/[i]}]["registration_points"]
            except:
                self.points_storage[{key/config["video_data"][i][title]}] = []
            """
            self.frame_label.mousePressEvent = lambda event: self.locationInImageCorner(
                event
            )
        print("go")
        layout.addWidget(self.frame_label)

        self.setLayout(layout)

    def set_image(self, image):
        h,w,ch = image.shape

        self.cornerImageDim = [w, h]
        if (h != self.height) or (w != self.width):
            self.height = h
            self.width = w
            
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        image = image.scaled(self.width, self.height, QtCore.Qt.KeepAspectRatio)
        pixmap = QPixmap(image)
        self.frame_label.setPixmap(pixmap)

    def locationInImageCorner(self, event):
        """When pressed will save place in image clicked and append to list however points won't be adjusted for the image so may not like what is imagined"""

        # try:
        if True:
            # print(self.sender())
            pos = str(event.pos())
            pos = pos.strip("PyQt5.QtCore.Qpoint")
            pos = pos.strip("()")
            print(pos)
            # info = openYaml()
            if len(pos) != 0:
        
                cord = pos.split(", ")
                cord[0] = int(
                    int(cord[0])
                    * self.cornerImageDim[0] #need dimension of the image before resizing
                    /self.frame_label.width()
                )
                cord[1] = int(
                    int(cord[1])
                    * self.cornerImageDim[1] #need dimension of the image before resizing
                    / self.frame_label.height() #divid
                )
                print(cord)
                #if len(self.points_storage[self.video_combo_box.combo_box.currentText()]) < 4:
                    # self.points_storage[self.video_combo_box.combo_box.currentText()].append(cord)
                # else:
                #   self.points_storage[self.video_combo_box.combo_box.currentText()][3] = cord
             
            
        # except:
        #     print("fail 565739274")

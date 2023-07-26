import numpy as np
import os
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy, QComboBox

class EmptyQVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

class EmptyQHBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

class MaterialPushButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setProperty('class', 'material-button')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

class MaterialLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setProperty('class', 'material-label')

class MaterialLineEdit(QWidget):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__()

        self.vbox_layout = EmptyQVBoxLayout()
        self.label = MaterialLabel(label_text)
        self.vbox_layout.addWidget(self.label)
        
        self.hbox_layout = EmptyQHBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(default_line_edit)
        self.hbox_layout.addWidget(self.line_edit)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.main_widget)

        self.setLayout(self.vbox_layout)

class MaterialComboBox(QWidget):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__()

        self.vbox_layout = EmptyQVBoxLayout()
        self.label = MaterialLabel(label_text)
        self.vbox_layout.addWidget(self.label)
        
        self.hbox_layout = EmptyQHBoxLayout()
        self.combo_box = QComboBox()
        self.hbox_layout.addWidget(self.combo_box)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.main_widget)

        self.setLayout(self.vbox_layout)

class MaterialFolderBrowseEdit(MaterialLineEdit):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__(label_text, default_line_edit)
        self.browse_button = MaterialPushButton("BROWSE")
        self.hbox_layout.addWidget(self.browse_button)
        self.browse_button.clicked.connect(self.browse)

    def browse(self):
        path = QFileDialog.getExistingDirectory(
            self, "Open the location of the folder", r"" + str(os.getcwd()))

        self.line_edit.setText(path)

class MaterialFileBrowseEdit(MaterialLineEdit):
    def __init__(self, label_text="", default_line_edit=""):
        super().__init__(label_text, default_line_edit)
        self.browse_button = MaterialPushButton("BROWSE")
        self.hbox_layout.addWidget(self.browse_button)

class MaterialLabelImage(QWidget):
    def __init__(self, label_text="", height=320, width=480):
        super().__init__()

        layout = EmptyQVBoxLayout()
        layout.addWidget(MaterialLabel(label_text))

        self.frame_label = QLabel()
        self.height = height
        self.width = width
        placeholder_frame = np.zeros(shape=(self.height,self.width,3), dtype=np.uint8)
        self.set_image(placeholder_frame)
        layout.addWidget(self.frame_label)

        self.setLayout(layout)

    def set_image(self, image):
        h,w,ch = image.shape
        if (h != self.height) or (w != self.width):
            self.height = h
            self.width = w
            
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        image = image.scaled(self.width, self.height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        pixmap = QPixmap(image)
        self.frame_label.setPixmap(pixmap)


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
  
        layout.addWidget(self.frame_label)

        self.setLayout(layout)

    def set_image(self, image):
        h,w,ch = image.shape

        self.cornerImageDim = [w, h]
        if (h != self.height) or (w != self.width):
            self.height = h
            self.width = w
            
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        image = image.scaled(self.width, self.height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        pixmap = QPixmap(image)
        self.frame_label.setPixmap(pixmap)

    def locationInImageCorner(self, event):
        """When pressed will save place in image clicked and append to list however points won't be adjusted for the image so may not like what is imagined"""

        # try:
        if True:
            # print(self.sender())
            pos = str(event.pos())
            pos = pos.strip("PyQt6.QtCore.Qpoint")
            pos = pos.strip("()")
     
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

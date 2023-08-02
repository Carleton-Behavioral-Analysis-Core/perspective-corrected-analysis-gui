import numpy as np
import os
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap, QPen, QColor
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy, QComboBox
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter
import logging

logger = logging.getLogger(__name__)

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
        self.browse_button.clicked.connect(self.browse)


    def browse(self):
        path = QFileDialog.getExistingDirectory(
            self, "Open the location of the folder", r"" + str(os.getcwd()))

        self.line_edit.setText(path)

class MaterialLabelImage(QWidget):
    mouseclick_signal = QtCore.pyqtSignal([int, int])

    def __init__(self, label_text="", max_height=320, max_width=480,Clickable=True):
        super().__init__()

        layout = EmptyQVBoxLayout()
        layout.addWidget(MaterialLabel(label_text))

        self.frame_label = QLabel()
        self.max_height = max_height
        self.max_width = max_width
        placeholder = np.zeros(shape=(self.max_height,self.max_width,3), dtype=np.uint8)
        self.set_image(placeholder)
        layout.addWidget(self.frame_label)

        self.setLayout(layout)
        if Clickable:
            self.frame_label.mousePressEvent = self.mouse_press_event_handler

    def set_image(self, image=None):
        if image is not None:
            self.image_height, self.image_width, self.image_channels = image.shape
            self.scale_ratio = min(self.max_height/self.image_height, self.max_width/self.image_width)
            self.width = int(self.image_width * self.scale_ratio)
            self.height = int(self.image_height * self.scale_ratio)
            self.bytes_per_line = self.image_channels * self.image_width
            self.base_image = image
            self.image = QImage(
                image.data, 
                self.image_width, 
                self.image_height, 
                self.bytes_per_line, 
                QImage.Format.Format_RGB888)

            self.image = self.image.scaled(self.width, self.height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        self.pixmap = QPixmap(self.image)
        self.frame_label.setPixmap(self.pixmap)
        
    def add_point(self, x, y, color, width=10):
        x = int(x * self.scale_ratio)
        y = int(y * self.scale_ratio)
        painter = QPainter(self.pixmap)
        pen = QPen(QColor(*color))
        pen.setWidth(width)
        painter.setPen(pen)
        points = QPoint(x,y)
        painter.drawPoint(x, y)
        painter.end()

    def clean(self):
        self.pixmap = QPixmap(self.image)

    def update(self):
        self.frame_label.setPixmap(self.pixmap)

    def mouse_press_event_handler(self, event):
        point = event.pos()
        x = int(point.x() / self.scale_ratio)
        y = int(point.y() / self.scale_ratio)
        logger.info("Label image clicked x=%i, y=%i", x, y)
        self.mouseclick_signal.emit(x, y)
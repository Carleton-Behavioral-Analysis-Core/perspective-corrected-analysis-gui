from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class CreateProjectTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Demo'))
        self.setLayout(layout)
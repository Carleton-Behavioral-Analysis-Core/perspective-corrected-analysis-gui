import sys

import tabs
from tabs.create_project import CreateProjectTab

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Andre, Argel & Aidan's amazingly awesome array alignment"
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_tabs()

        self.setCentralWidget(self.tab_widget)
        self.show()

    def create_tabs(self):
        self.tab_widget = QTabWidget()
        self.create_project_tab = tabs.create_project.CreateProjectTab()
        self.tab_widget.addTab(self.create_project_tab, "Tab Name")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
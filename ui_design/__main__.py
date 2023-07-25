import sys

from tabs import load_project, create_project, load_videos, registration
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Andre, Aiden"
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Load the gloval stylesheet
        with open(Path(__file__).parent / 'stylesheet.css', 'r') as fp:
            self.setStyleSheet(fp.read())

        self.create_tabs()
        self.setCentralWidget(self.tab_widget)
        self.show()

    def create_tabs(self):
        self.tab_widget = QTabWidget()

        # Add the create project tab
        self.create_project_tab = create_project.CreateProjectTab()
        self.tab_widget.addTab(self.create_project_tab, "Create Project")

        self.load_project_tab = load_project.LoadProjectTab()
        self.tab_widget.addTab(self.load_project_tab, "Load Project")

        self.load_videos_tab = load_videos.LoadVideosTab()
        self.tab_widget.addTab(self.load_videos_tab, "Load Videos")

        self.registration_tab = registration.RegistrationTab()
        self.tab_widget.addTab(self.registration_tab, "Register")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
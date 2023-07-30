import sys
import logging

from tabs import load_project, create_project, load_videos, registration, analysis
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
from ui_design.model import Model

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Analysis Application"
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.model = Model()

        # Load the gloval stylesheet
        with open(Path(__file__).parent / 'stylesheet.css', 'r') as fp:
            self.setStyleSheet(fp.read())

        self.create_tabs()
        self.setCentralWidget(self.tab_widget)
        self.show()

    def create_tabs(self):
        self.tab_widget = QTabWidget()

        # Add the create project tab
        self.create_project_tab = create_project.CreateProjectTab(self.model)
        self.tab_widget.addTab(self.create_project_tab, "Create Project")

        self.load_project_tab = load_project.LoadProjectTab(self.model)
        self.tab_widget.addTab(self.load_project_tab, "Load Project")

        self.load_videos_tab = load_videos.LoadVideosTab(self.model)
        self.tab_widget.addTab(self.load_videos_tab, "Load Videos")

        self.registration_tab = registration.RegistrationTab(self.model)
        self.tab_widget.addTab(self.registration_tab, "Register")

        self.analysis_tab = analysis.AnalysisTab(self.model)
        self.tab_widget.addTab(self.analysis_tab, "Analysis")

        # self.analysis_tab = analysis.AnalysisTab(self.model)
        # self.tab_widget.addTab(self.analysis_tab, "Results")

if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
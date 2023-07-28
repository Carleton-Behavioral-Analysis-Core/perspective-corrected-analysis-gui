from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox
from ruamel.yaml import YAML
from pathlib import Path
import logging
import cv2
from collections import OrderedDict
from ruamel.yaml.comments import CommentedMap as ordereddict

class Model(QObject):
    config_changed_signal = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.config = None 
        self.config_path = None
        self._yaml_parser = YAML()
        self.logger = logging.getLogger(__name__)

    def load_config(self, give_confirmation_message=True):
        config_path = self.get_config_path()
        self.config = self._yaml_parser.load(self.config_path)
        self.logger.info("Loaded config")
        
        self.logger.info("Emit signal that project config has updated")
        self.config_changed_signal.emit()

        if give_confirmation_message:
            QMessageBox(
                QMessageBox.Icon.Information,
                "Project Loaded Successfully",
                f"The project has loaded from {config_path} successfully",
                QMessageBox.StandardButton.Ok
            ).exec()

    def dump_config(self):
        config_path = self.get_config_path()
        with open(config_path, 'w') as fp:
            self._yaml_parser.dump(self.config, fp)

        self.load_config(give_confirmation_message=False)

    def get_config_path(self):
        if self.config_path is not None:
            config_path = Path(self.config_path)
            if config_path.exists():
                return config_path
            else:
                self.logger.error("Config path does not exist")
        else:
            self.logger.error("config.yaml path not set")
        
    def create_project(self, folder, name):
        template_path = Path(__file__).parent / 'template.yaml'
        config = self._yaml_parser.load(template_path)

        project_path = Path(folder) / name
        project_path = project_path.resolve()
        self.logger.info("Creating new project at %s", project_path)
        if not project_path.exists():
            project_path.mkdir(parents=True)

        self.logger.info("Creating config.yaml from template.yaml")
        self.config_path = project_path / 'config.yaml'
        self._yaml_parser.dump(config, self.config_path)

        self.logger.info("Loading created project")
        self.load_config()

    def load_project(self, project_path):
        self.logger.info("Loading existing project from %s", project_path)
        project_path = Path(project_path)
        config_path = project_path / 'config.yaml'
        if not config_path.exists():
            self.logger.error("Config path does not exist at %s", config_path)

        self.config_path = config_path
        self.load_config()

    def load_videos_and_dlc_files(self, video_folder, dlc_folder):
        video_folder = Path(video_folder)
        dlc_folder = Path(dlc_folder)

        videos = (
            list(video_folder.glob('*.mp4')) + 
            list(video_folder.glob('*.MP4'))
        )

        # TODO exception if no videos were found
        video_data = OrderedDict()
        for video in videos:
            key = video.parts[-1]
            fname, _ = key.split('.')
            if key in self.config['video_data']:
                video_data[key] = self.config['video_data'][key]
                continue

            dlc_file = next(dlc_folder.glob(f"{fname}DLC*.h5")).parts[-1]
            dlc_video = next(dlc_folder.glob(f"{fname}DLC*_labeled.mp4")).parts[-1]

            cap = cv2.VideoCapture(str(video))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = float(cap.get(cv2.CAP_PROP_FPS))
            
            groups = []
            registration_points = [
                [0,0],
                [width,0],
                [width,height],
                [0,height]
            ]

            video_data[key] = (ordereddict([
                ('dlc_file', str(dlc_file)),
                ('dlc_video', str(dlc_video)),
                ('video_width', width),
                ('video_height', height),
                ('video_fps', fps),
                ('groups', groups),
                ('registration_points', registration_points)
            ]))

        self.logger.info('Saving to config')
        self.config['video_data'] = video_data
        self.config['video_folder_path'] = str(video_folder)
        self.config['dlc_folder_path'] = str(dlc_folder)
        self.config['video_data'] = video_data
        self.dump_config()
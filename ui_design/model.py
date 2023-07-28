from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from ruamel.yaml import YAML
from pathlib import Path
import logging

class Model(QObject):
    config_changed = QtCore.pyqtSignal()
    
    def __init__(self):
        self.config = None 
        self.config_path = None
        self._yaml_parser = YAML()
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        config_path = self.get_config_path()
        self.config = self._yaml_parser.load(self.config_path)
        self.logger.info("Loaded config")

    def update_config(self, config):
        config_path = self.get_config_path()
        with open(config_path, 'w') as fp:
            self._yaml_parser.dump(config, fp)

        self.load_config()
        
        self.logger.info("Emit signal that project config has updated")
        self.config_changed.emit()

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

        self.logger.info("Emit signal that project config has updated")
        self.config_changed.emit()

    def load_project(self, project_path):
        self.logger.info("Loading existing project from %s", project_path)
        project_path = Path(project_path)
        config_path = project_path / 'config.yaml'
        if not config_path.exists():
            self.logger.error("Config path does not exist at %s", config_path)

        self.config_path = config_path
        self.load_config()

        self.logger.info("Emit signal that project config has updated")
        self.config_changed.emit()
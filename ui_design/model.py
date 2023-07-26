from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from ruamel.yaml import YAML
from pathlib import Path

class Model(QObject):
    config_changed = QtCore.pyqtSignal()

    def __init__(self):
        self._config = None 
        self._config_path = None
        self._yaml_parser = YAML()

    def get_config(self):
        config_path = self.get_config_path()
        return self._yaml_parser.load(self._config_path)

    def update_config(self, config):
        config_path = self.get_config_path()
        with open(config_path, 'w') as fp:
            self._yaml_parser.dump(config, fp)

    def get_config_path(self):
        if self._config_path is not None:
            config_path = Path(self._config_path)
            if config_path.exists():
                return config_path
            else:
                raise Exception("Config path does not exist")
        else:
            raise Exception("config.yaml path not set")

    def update_config_path(self, config_path):
        config_path = Path(config_path)
        if not config_path.exists():
            raise Exception("Config path does not exist")
            return

        self._config_path = config_path
        
    def create_project(self, folder, name):
        template_path = Path(__file__).parent / 'template.yaml'
        config = self._yaml_parser.load(template_path)

        project_path = Path(folder) / name
        if not project_path.exists():
            project_path.mkdir(parents=True)

        self._yaml_parser.dump(config, project_path / 'config.yaml')
from PyQt6.QtCore import QObject
from ruamel.yaml import YAML

model = Model()
model.config_changed.connect()

class Model(QObject):
    config_changed = QtCore.pyqtSignal()

    def __init__(self):
        self._config = None 
        self._config_path = None
        self._yaml_parser = YAML()

    def get_config(self):
        if self._config_path is not None:
            assert self._config_path.exists(), "Config path does not exist"
            return self._yaml_parser.load(self._config_path)
        else:
            raise Exception("config.yaml path not set")

    # def update_config(self, config):
    #     with open() 
    #     self._yaml_parser.dump

    # def get_config_path(self):
    #     pass

    # def update_config_path(self, config):
    #     with open()
    #     self._yaml_parser.dump
import os
from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox
from ruamel.yaml import YAML
from pathlib import Path
import logging
import cv2
from collections import OrderedDict
from ruamel.yaml.comments import CommentedMap as ordereddict
from behavior_analysis_tool.analysis import *
from scipy.stats.kde import gaussian_kde

class Model(QObject):
    config_changed_signal = QtCore.pyqtSignal()
    analysis_changed_signal = QtCore.pyqtSignal()
    progressbar_changed_signal = QtCore.pyqtSignal(int)
    # TODO create a new signal for analysis progress

    def __init__(self):
        super().__init__()
        self.config = None 
        self.config_path = None
        self._yaml_parser = YAML()
        self.logger = logging.getLogger(__name__)

    def load_config(self, give_confirmation_message=True):
        config_path = self.get_config_path()
        if config_path != None and os.path.exists(config_path) and config_path != "...":
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
        else:
            logger.warn("Path: " + str(config_path) + " is invalid ")
            QMessageBox(
                    QMessageBox.Icon.Information,
                    "Project Failed To Load Config File",
                    f"The Path {config_path} is Invalid",
                    QMessageBox.StandardButton.Ok
                ).exec()


    def dump_config(self):
        config_path = self.get_config_path()
        with open(config_path, 'w') as fp:
            self._yaml_parser.dump(self.config, fp)

        self.load_config(give_confirmation_message=False)

    def get_schema(self):
        height = self.config['box_height']
        width = self.config['box_width']
        schema_points = np.array([
            [0,0],
            [width,0],
            [width,height],
            [0,height]
        ]).astype(np.float32)
        return schema_points

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
     
        if config_path.exists() and config_path != None and os.path.exists(config_path) and config_path != "..." and config_path != ".." and config_path != ".":
            self.config_path = config_path
            self.load_config()
            
        else:
            self.logger.error("Config path does not exist at %s", config_path)
            QMessageBox(
                    QMessageBox.Icon.Information,
                    "Project Failed To Load Config File",
                    f"The Path {config_path} is Invalid",
                    QMessageBox.StandardButton.Ok
                ).exec()

    def load_videos_and_dlc_files(self, video_folder, dlc_folder):
        video_folder = Path(video_folder)
        dlc_folder = Path(dlc_folder)

        self.config['video_folder_path'] = str(video_folder)
        self.config['dlc_folder_path'] = str(dlc_folder)

        videos = (
            list(video_folder.glob('*.mp4')) + 
            list(video_folder.glob('*.MP4'))
        )

        # TODO exception if no videos were found
        video_data = OrderedDict()
        for video in videos:
            try:
                key = video.parts[-1]
                fname, _ = key.split('.')
                if key in self.config['video_data']:
                    video_data[key] = self.config['video_data'][key]
                    continue

                dlc_file = next(dlc_folder.glob(f"{fname}DLC*.h5")).parts[-1]
                dlc_video = next(dlc_folder.glob(f"{fname}DLC*_labeled.mp4")).parts[-1]
                groups = []
                video_info = self.get_video_info(key)
                width = video_info['width']
                height = video_info['height']
                registration_points = [
                    [0,0],
                    [width,0],
                    [width,height],
                    [0,height]
                ]

                video_data[key] = (ordereddict([
                    ('dlc_file', str(dlc_file)),
                    ('dlc_video', str(dlc_video)),
                    ('groups', groups),
                    ('registration_points', registration_points)
                ]))
            except:
                pass

        # find the minimum number of frames in the video
        min_frames = min([self.get_video_info(v)['fps'] for v in videos])
        
        self.logger.info('Saving to config')
        self.config['video_data'] = video_data
        
        self.dump_config()

    def register_measurements(self,width,height):
        self.config['box_height'] = height
        self.config['box_width'] = width
        self.dump_config()

    def get_video_info(self, video):
        video = Path(self.config['video_folder_path']) / video
        cap = cv2.VideoCapture(str(video))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return {
            'width': width,
            'height': height,
            'fps': fps,
            'frames': frames
        }

    def perform_analysis(self):
        if self.config_path != None and os.path.exists(self.config_path) and os.path.exists(self.config['video_folder_path']) and os.path.exists(self.config['dlc_folder_path']):
            self.logger.info("Started analysis")
            self.load_config(False)

            videos = self.config['video_data']
            all_video_analysis = []
            self.progressbar_changed_signal.emit(int(3))
            num_videos = len(videos) 
            print(num_videos)
            video_counter = 1
            for counter, video in enumerate(videos):
             
                # self.progressbar_changed_signal.emit(int(counter))
                self.logger.info("Started analysis on video %s [%i/%i]", video, counter, len(videos))
                video_analysis = VideoAnalysis(video, self)
                video_analysis.process()
                all_video_analysis.append(video_analysis)
                self.progressbar_changed_signal.emit(int(((90/num_videos)*video_counter))+3)
                video_counter += 1
            
            self.logger.info("Saving results")
            result_df = pd.DataFrame([va.results for va in all_video_analysis])
            result_df.to_csv(Path(self.config_path).parent / 'results.csv')
            
            self.logger.info("Creating group heatmaps")
            self.progressbar_changed_signal.emit(int(97))
            for group in self.config['treatment_groups']:
               
                group_analysis = [va for va in all_video_analysis if group in va.video_groups]
                if not len(group_analysis):
                    continue
                centroids = [va.centroid for va in group_analysis]
                centroids = pd.concat(centroids, axis=0).dropna()
                data = centroids[['y', 'x']].values.T
                k = gaussian_kde(data[:,::10], )
                mgrid = np.mgrid[:self.config['box_height'], :self.config['box_width']]
                z = k(mgrid.reshape(2, -1))
                plt.title(f"Heatmap ({group})")
                plt.imshow(group_analysis[0].representative_frame)
                contour_levels = 20
                plt.contourf(z.reshape(mgrid.shape[1:]), cmap='seismic', alpha=1, levels=contour_levels)
                folder = Path(self.config_path).parent / 'figures/group_heatmaps'
                if not folder.exists():
                    folder.mkdir(parents=True)
                plt.tight_layout()
                plt.savefig(folder / f"{group}.png")
                plt.savefig(folder / f"{group}.pdf")
                plt.close()
            
            self.logger.info("Analysis complete")
            self.progressbar_changed_signal.emit(int(100))
            self.analysis_changed_signal.emit()
        elif self.config_path == None or not os.path.exists(self.config_path):
            logger.warn("No Path to Config File Found")
        elif not os.path.exists(self.config['video_folder_path']):
            logger.warn("No Path to Video Folder Found")
        elif not os.path.exists(self.config['video_folder_path']):
            logger.warn("No Path to DLC Video Folder Found")
        


    def create_default_analysis_zones(self):
        if self.config_path != None and os.path.exists(self.config_path) and os.path.exists(self.config['video_folder_path']) and os.path.exists(self.config['dlc_folder_path']):
            width = self.config['box_width']
            height = self.config['box_height']
            overflow = 25 
            padding = 80
            zones = ordereddict()

            self.logger.info("Creating default analysis zones")
            zones["centre"] = [
                [padding,padding],
                [width-padding,padding],
                [width-padding,height-padding],
                [padding,height-padding]
            ]

            zones["outer"] = [
                [-overflow,-overflow],
                [width+overflow,-overflow],
                [width+overflow,height+overflow],
                [-overflow,height+overflow]
            ]

            x0 = -overflow
            x1 = padding
            y0 = -overflow
            y1 = padding
            zones["top_left_corner"] = [
                [x0, y0],
                [x1, y0],
                [x1, y1],
                [x0, y1]
            ]

            x0 = width-padding
            x1 = width+overflow
            y0 = -overflow
            y1 = padding
            zones["top_right_corner"] = [
                [x0, y0],
                [x1, y0],
                [x1, y1],
                [x0, y1]
            ]

            x0 = width-padding
            x1 = width+overflow
            y0 = height-padding
            y1 = height+overflow
            zones["bottom_right_corner"] = [
                [x0, y0],
                [x1, y0],
                [x1, y1],
                [x0, y1]
            ]

            x0 = -overflow
            x1 = padding
            y0 = height-padding
            y1 = height+overflow
            zones["bottom_left_corner"] = [
                [x0, y0],
                [x1, y0],
                [x1, y1],
                [x0, y1]
            ]

            self.config['zones'] = zones
            self.dump_config()


        elif self.config_path == None or not os.path.exists(self.config_path):
            logger.warn("No Path to Config File Found")
        elif not os.path.exists(self.config['video_folder_path']):
            logger.warn("No Path to Video Folder Found")
        elif not os.path.exists(self.config['video_folder_path']):
            logger.warn("No Path to DLC Video Folder Found")

        
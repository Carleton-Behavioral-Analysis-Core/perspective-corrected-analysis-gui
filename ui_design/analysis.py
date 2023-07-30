import logging
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde
from ui_design.utils import *
from ruamel.yaml.comments import CommentedMap as ordereddict
from pathlib import Path

logger = logging.getLogger(__name__)

class VideoAnalysis:
    """Analyze a single experiment"""
    def __init__(self, video, model):
        self.video = video
        self.model = model
        self.fname = video.split('.')[0]
        self.video_groups = self.model.config['video_data'][self.video]['groups']
        self.results = ordereddict()

    def load_keypoints(self):
        dlc_folder = Path(self.model.config['dlc_folder_path'])
        dlc_file = self.model.config['video_data'][self.video]['dlc_file']
        dlc_full_filepath = dlc_folder / dlc_file

        logger.info('Loading full DeepLabCut file from %s', dlc_full_filepath)
        self.raw_keypoints = pd.read_hdf(dlc_full_filepath)

        logger.info('Finding homogeneous transform')
        self.transform = self.get_registration_transform()

        logger.info('Transforming keypoints to new perspective')
        self.keypoints = transform_dataframe_to_perspective(self.raw_keypoints, self.transform)

        logger.info('Dropping low likelihood parts')
        likelihood = self.keypoints.xs('likelihood', level='coords', axis=1)
        pcutoff = self.model.config['dlc_pcutoff']
        self.keypoints = self.keypoints.where(likelihood > pcutoff)

        logger.info('Interpolate')
        self.keypoints = self.keypoints.interpolate()

        logger.info('Find centroid')
        self.centroid = self.keypoints.groupby(level='coords', axis=1).mean()

        logger.info('Find start and end frames')
        video_info = self.model.get_video_info(self.video)
        self.fps = int(video_info['fps'])
        analysis_start_time_in_seconds = float(self.model.config['analysis_start_time_in_seconds'])
        self.analysis_start_frame = int(analysis_start_time_in_seconds * self.fps)
        analysis_end_time_in_seconds = float(self.model.config['analysis_end_time_in_seconds'])
        self.analysis_end_frame = int(analysis_end_time_in_seconds * self.fps)
        self.centroid = self.centroid.loc[self.analysis_start_frame:self.analysis_end_frame].dropna()

    def process_distance_metrics(self):
        logger.info('Calculate total distance')
        deltas = self.centroid.diff().dropna()
        deltas = deltas[['x','y']]
        distances = np.linalg.norm(deltas.values, axis=1)
        distances[distances > self.model.config['threshold']] = 0
        smoothed_distance_per_frame = pd.Series(distances).rolling(self.fps*3, center=True).mean().fillna(0)
        total_distance = round(distances.sum()) / 1000
        logger.info('Distance %im', total_distance)
        self.results['distance'] = total_distance

        logger.info('Creating distance traveled plots')
        plt.figure(figsize=(8,4))
        # Average over 3s
        speed = smoothed_distance_per_frame * self.fps
        plt.plot(speed)
        plt.ylabel("Speed [mm/s]")
        plt.xlabel("Frame")
        plt.title(f"Distance Traveled ({self.fname})")
        folder = Path(self.model.config_path).parent / 'figures/distance'
        if not folder.exists():
            folder.mkdir(parents=True)

        plt.tight_layout()
        plt.savefig(folder / f"{self.fname}.png")
        plt.savefig(folder / f"{self.fname}.pdf")
        plt.close()

        logger.info('Cumulative distance')
        plt.figure(figsize=(8,4))
        cumulative_distances = np.zeros_like(distances)
        cumulative_distance_counter = 0
        for i, distance in enumerate(smoothed_distance_per_frame):
            cumulative_distance_counter += distance
            cumulative_distances[i] = cumulative_distance_counter

        plt.plot(cumulative_distances)
        plt.ylabel("Cumulative Distance [mm]")
        plt.xlabel("Frame")
        plt.title(f"Cumulative Distance Traveled ({self.fname})")
        folder = Path(self.model.config_path).parent / 'figures/cumulative_distance'
        if not folder.exists():
            folder.mkdir(parents=True)
        plt.tight_layout()
        plt.savefig(folder / f"{self.fname}.png")
        plt.savefig(folder / f"{self.fname}.pdf")
        plt.close()


    def process_zone_metrics(self):
        logger.info('Processing zone metrics')

        zones = self.model.config['zones']
        zone_colors = plt.get_cmap('rainbow')(np.linspace(0,1,len(zones)))

        logger.info('Calculate time in zones')
        for zone in zones:
            points = np.array(self.model.config['zones'][zone])
            zone_polygon = plt.Polygon(points)
            in_zone = zone_polygon.contains_points(self.centroid[['x', 'y']].values)
            time_in_zone = round(in_zone.sum() / self.fps, 2)
            logger.info('Time in zone %s: %i', zone, time_in_zone)
            self.results[f"time_in_{zone}"] = time_in_zone

        logger.info('Plotting time in each zone')
        height_per_zone = 2
        gs = plt.GridSpec(len(zones), 1)
        plt.figure(figsize=(8, height_per_zone*len(zones)))
        plt.suptitle('Time Spent in Zones')
        ax = None
        for zone_idx, zone in enumerate(zones):
            points = np.array(self.model.config['zones'][zone])
            zone_polygon = plt.Polygon(points, label=zone)
            in_zone = zone_polygon.contains_points(self.centroid[['x', 'y']].values)
            ax = plt.subplot(gs[zone_idx], sharex=ax)
            plt.plot(in_zone, color=zone_colors[zone_idx])
            plt.fill_between(np.arange(len(in_zone)), 0, in_zone, color=zone_colors[zone_idx], alpha=0.5)
            plt.ylabel(zone)
            plt.yticks([0,1], ['outside', 'inside'])
        plt.xlabel("Frame")
        folder = Path(self.model.config_path).parent / 'figures/time_in_zones'
        if not folder.exists():
            folder.mkdir(parents=True)
        plt.tight_layout()
        plt.savefig(folder / f"{self.fname}.png")
        plt.savefig(folder / f"{self.fname}.pdf")
        plt.close()
        
        logger.info('Creating zone plots')
        plt.figure(figsize=(8,8))
        plt.imshow(self.representative_frame)
        for zone_idx, zone in enumerate(zones):
            points = np.array(self.model.config['zones'][zone])
            zone_polygon = plt.Polygon(points, color=zone_colors[zone_idx], label=zone, alpha=0.3)
            plt.gca().add_patch(zone_polygon)
        c = np.linspace(0,1,len(self.centroid))
        plt.scatter(self.centroid.x, self.centroid.y, s=3, c=c)
        plt.xlim([0,self.width])
        plt.ylim([self.height,0])
        plt.title(f"Zone Plots ({self.fname})")
        plt.xlabel("Width [mm]")
        plt.ylabel("Height [mm]")
        plt.legend()
        folder = Path(self.model.config_path).parent / 'figures/zones'
        if not folder.exists():
            folder.mkdir(parents=True)
        plt.tight_layout()
        plt.savefig(folder / f"{self.fname}.png")
        plt.savefig(folder / f"{self.fname}.pdf")
        plt.close()


    def process(self):
        self.results = ordereddict()
        self.results['video'] = self.video

        self.load_keypoints()

        self.video_folder = Path(self.model.config['video_folder_path'])
        self.video_reader = VideoReader(self.video_folder / self.video)
        frame_index = len(self.video_reader) // 2
        logger.info('Getting representative frame for plotting, choosing frame %i', frame_index)
        self.height = round(self.model.config['box_height'])
        self.width = round(self.model.config['box_width'])
        self.representative_frame = cv2.warpPerspective(
            self.video_reader[frame_index], self.transform, dsize=(self.width,self.height))

        logger.info("Identifying groups")
        video_data = self.model.config['video_data'][self.video]
        all_groups = self.model.config['treatment_groups']
        video_groups = video_data['groups']
        for group in all_groups:
            self.results[group] = group in video_groups

        logger.info('Getting distance metrics')
        distance_metrics = self.process_distance_metrics()

        logger.info('Getting zone metrics')
        zone_metrics = self.process_zone_metrics()

        logger.info('Creating tracking plots')
        plt.figure(figsize=(8,8))
        plt.imshow(self.representative_frame)
        plt.scatter(self.centroid.x, self.centroid.y, s=2, c=np.linspace(0,1,len(self.centroid)))
        plt.xlim([0,self.width])
        plt.ylim([self.height,0])
        plt.xlabel("Width [mm]")
        plt.ylabel("Height [mm]")
        plt.title(f"Tracks ({self.fname})")
        folder = Path(self.model.config_path).parent / 'figures/tracking'
        if not folder.exists():
            folder.mkdir(parents=True)
        plt.tight_layout()
        plt.savefig(folder / f"{self.fname}.png")
        plt.savefig(folder / f"{self.fname}.pdf")
        plt.close()

        logger.info('Producing heatmaps')
        from scipy.stats.kde import gaussian_kde
        plt.figure(figsize=(8,8))
        plt.xlabel("Width [mm]")
        plt.ylabel("Height [mm]")
        heatmap_alpha=1.0 # TODO move these into the configuration
        sample_every_n_frames=10
        contour_levels=20
        data = self.centroid[['y', 'x']].values.T
        k = gaussian_kde(data[:,::sample_every_n_frames])
        mgrid = np.mgrid[:self.height, :self.width]
        z = k(mgrid.reshape(2, -1))
        plt.title(f"Heatmap ({self.fname})")
        plt.imshow(self.representative_frame)
        plt.contourf(z.reshape(mgrid.shape[1:]), cmap='seismic', alpha=1, levels=contour_levels)
        folder = Path(self.model.config_path).parent / 'figures/heatmaps'
        if not folder.exists():
            folder.mkdir(parents=True)
        plt.tight_layout()
        plt.savefig(folder / f"{self.fname}.png")
        plt.savefig(folder / f"{self.fname}.pdf")
        plt.close()


    def get_registration_transform(self):
        video_info = self.model.config['video_data'][self.video]
        registration_points = np.array(video_info['registration_points']).astype(np.float32)
        schema_points = self.model.get_schema()
        logger.info('Found registration')
        return cv2.getPerspectiveTransform(registration_points, schema_points)
import logging
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt

from pathlib import Path

logger = logging.getLogger(__name__)

def transform_array_to_perspective(arr, T):
    """Move into the box's frame of reference"""
    x, y = arr.T
    tx, ty, v = T @ np.c_[x, y, np.ones_like(x)].T
    return np.c_[tx / v, ty / v]

def transform_dataframe_to_perspective(df, T):
    """Transform the coordinate dataframes to be in the box's frame of reference"""
    df = df.copy().dropna()
    idx = pd.IndexSlice
    x = df.loc[:, idx[:, :, "x"]]
    y = df.loc[:, idx[:, :, "y"]]
    x = x.stack(dropna=False).stack(dropna=False)
    y = y.stack(dropna=False).stack(dropna=False)

    tx, ty, v = T @ np.c_[x, y, np.ones_like(x)].T
    tx = tx / v
    ty = ty / v

    tx = pd.DataFrame(tx, index=x.index, columns=x.columns).unstack().unstack()
    ty = pd.DataFrame(ty, index=y.index, columns=y.columns).unstack().unstack()

    # Update multi index columns to match
    df.loc[:, pd.IndexSlice[:, :, "x"]] = tx
    df.loc[:, pd.IndexSlice[:, :, "y"]] = ty
    return df

def get_homography(points, target):
    T, res = cv2.findHomography(
        points, target, cv2.RANSAC, ransacReprojThreshold=32)
    return T

class VideoReader:
    def __init__(self, video):
        video = str(video)
        self.video = video
        self.fname = get_fname(video)
        self.cap = cv2.VideoCapture(video)
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.fps = float(self.cap.get(cv2.CAP_PROP_FPS))
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.pos = 0
        
    def __getitem__(self, idx):
        if idx >= self.frames or idx < 0:
            raise IndexError("Out of bounds")
            
        if self.pos != idx:
            assert self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            self.pos = idx
        
        ret, frame = self.cap.read()
        self.pos += 1
        frame = np.flip(frame, 2)
        return frame
    
    def __len__(self):
        return self.frames
    
    def __del__(self):
        self.cap.release()
    
class VideoWriter:
    def __init__(self, video, fps, width, height):
        self.video = str(video)
        self.fname = Path(self.video).parts[-1].split('.')[0]
        self.fps = fps
        self.width = width
        self.height = height
        self.writer = None
        
    def __enter__(self):
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.writer = cv2.VideoWriter(self.video, fourcc, self.fps, (self.width, self.height))
        return self
    
    def write(self, frame):
        frame = np.flip(frame)
        self.writer.write(frame)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.release()

class VideoAnalysis:
    def __init__(self, video, model):
        self.video = video
        self.model = model

    def run(self):
        logger.info('Load dlc keypoints')
        dlc_folder = Path(self.model.config['dlc_folder_path'])
        dlc_file = self.model.config['video_data'][self.video]['dlc_file']
        dlc_full_filepath = dlc_folder / dlc_file

        logger.info('Loading full dlc file from %s', dlc_full_filepath)
        keypoints = pd.read_hdf(dlc_full_filepath)

        logger.info('Finding homogeneous transform')
        transform = self.get_registration_transform()

        logger.info('Transforming keypoints to new perspective')
        keypoints = transform_dataframe_to_perspective(keypoints, transform)

        logger.info('Dropping low likelihood parts')
        likelihood = keypoints.xs('likelihood', level='coords', axis=1)
        pcutoff = self.model.config['dlc_pcutoff']
        keypoints = keypoints.where(likelihood > pcutoff)

        logger.info('Interpolate')
        keypoints = keypoints.interpolate()

        logger.info('Find centroid')
        centroid = keypoints.groupby(level='coords', axis=1).mean()

        logger.info('Find start and end frames')
        video_info = self.model.get_video_info(self.video)
        fps = int(video_info['fps'])
        analysis_start_time_in_seconds = float(self.model.config['analysis_start_time_in_seconds'])
        analysis_start_frame = int(analysis_start_time_in_seconds * fps)
        analysis_end_time_in_seconds = float(self.model.config['analysis_end_time_in_seconds'])
        analysis_end_frame = int(analysis_end_time_in_seconds * fps)
        centroid = centroid.loc[analysis_start_frame:analysis_end_frame].dropna()

        logger.info('Calculate total distance')
        deltas = centroid.diff().dropna()
        deltas = deltas[['x','y']]
        distances = np.linalg.norm(deltas.values, axis=1) 
        logger.info('Distance %imm', round(distances.sum()))

        logger.info('Calculate time in zones ')
        zones = self.model.config['zones']
        for zone in zones:
            points = np.array(self.model.config['zones'][zone])

    def get_schema(self):
        height = self.model.config['box_height']
        width = self.model.config['box_width']
        schema_points = np.array([
            [0,0],
            [0,width],
            [height,width],
            [height,0]
        ]).astype(np.float32)
        return schema_points

    def get_registration_transform(self):
        video_info = self.model.config['video_data'][self.video]
        registration_points = np.array(video_info['registration_points']).astype(np.float32)
        schema_points = self.get_schema()
        logger.info('Found registration')
        return cv2.getPerspectiveTransform(registration_points, schema_points)
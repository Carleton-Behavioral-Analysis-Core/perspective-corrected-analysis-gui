import cv2
import numpy as np
import pandas as pd
from pathlib import Path

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
        return frame.astype(np.uint8)
    
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
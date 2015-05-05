import numpy as np
import cv2
import skvideo.io
from analysis import analyze

# cv2.VideoCapture is broken on Debian, probably due to missing ffmpeg
# skvideo.io works as a drop-in replacement.
# Install with'pip install scikit-video'

# Video must be in avi format
cap = skvideo.io.VideoCapture('../data/videos/sample.avi')

results = { 'activity': [], 'density': [] }

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        (cheer, dense) = analyze(frame, False)

        results['activity'].append(cheer)
        results['density'].append(dense)
    else:
        cap.release()

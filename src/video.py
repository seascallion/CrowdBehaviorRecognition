import numpy as np
import cv2
import skvideo.io
from analysis import analyze

# cv2.VideoCapture is broken on Debian, probably due to missing ffmpeg
# skvideo.io works as a drop-in replacement.
# Install with'pip install scikit-video'

# Video must be in avi format
cap = skvideo.io.VideoCapture('../data/videos/sample.avi')
while(cap.isOpened()):
    ret, frame = cap.read()

    (cheer, dense) = analyze(frame)

    print 'Cheering: ',cheer
    print 'Density:', dense
cap.release()


#! /usr/bin/env python
import numpy as np
import cv2
import skvideo.io
from analysis import analyze
import matplotlib.pyplot as plt

# cv2.VideoCapture is broken on Debian, probably due to missing ffmpeg
# skvideo.io works as a drop-in replacement.
# Install with'pip install scikit-video'

# Video must be in avi format
cap = skvideo.io.VideoCapture('../data/videos/sample.avi')

results = { 'activity': [], 'density': [] }
frames = 0

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        (cheer, dense) = analyze(frame, False)

        results['activity'].append(cheer)
        results['density'].append(dense)
        frames += 1
    else:
        cap.release()

# Plot the activity and density over time
fig, ax1 = plt.subplots()
t = np.arange(0, frames, 1)
s1 = results['activity']
ax1.plot(t, s1, 'b-')
ax1.set_xlabel('frames')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Activity', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')


ax2 = ax1.twinx()
s2 = results['density']
ax2.plot(t, s2, 'r-')
ax2.set_ylabel('Density', color='r')
ax2.set_ylim([0, 0.1])
ax1.set_ylim([-1, 1])
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()

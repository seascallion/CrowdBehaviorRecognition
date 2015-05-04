#!/usr/bin/env python

import numpy as np
import cv2
from sys import argv

filename = argv[1]

hand_cascade = cv2.CascadeClassifier('../data/images/data/cascade.xml')

image = cv2.imread('../data/images/%s' % filename)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

hands = hand_cascade.detectMultiScale(image_gray, 1.3, 40)
for (x, y, w, h) in hands:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


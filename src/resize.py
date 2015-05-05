#! /usr/bin/env python
# Resize all the images in our dataset to 400x300, cropping if necessary

import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', default='data/images/sampleImages', help='Path to the images folder')

args = vars(ap.parse_args())

images_path = args['images']

image_paths = sorted([
    os.sep.join([images_path, filename])
    for filename in os.listdir(images_path)
    if any(filename.lower().endswith('.{0}'.format(ext)) for ext in ['jpg', 'jpeg', 'png'])
])

target_width, target_height = (640, 480)

for image_path in image_paths:
	image = cv2.imread(image_path)
	height, width, depth = image.shape
	if (width, height) == (target_width, target_height):
		continue
	if 1.0 * width / height > 4.0 / 3.0:
		image = cv2.resize(image, (width * target_height / height, target_height))
		height, width, depth = image.shape
		image = image[0:target_height, (width / 2 - target_width / 2):(width / 2 + target_width / 2)]
	else:
		image = cv2.resize(image, (target_width, height * target_width / width))
		height, width, depth = image.shape
		image = image[(height / 2 - target_height / 2):(height / 2 + target_height / 2), 0:target_width]
	cv2.imwrite(image_path, image)

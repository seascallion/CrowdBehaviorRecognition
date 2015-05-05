#! /usr/bin/env python
# Resize all the images in our dataset to 400x300, cropping if necessary

import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', default='data/images/sampleImages', help='Path to the images folder')

args = vars(ap.parse_args())

images_path = args['images']

target_width, target_height = (640, 480)

for root, dirs, files in os.walk(images_path):
	for filename in files:
		image_path = os.path.join(root, filename)
		print image_path
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

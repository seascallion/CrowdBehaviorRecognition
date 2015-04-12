import numpy as np
from cv2 import getStructuringElement, erode, dilate, cvtColor, inRange, GaussianBlur, bitwise_and, COLOR_BGR2HSV, MORPH_ELLIPSE

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
# TODO: figure out what range to use
# AND figure out why this doesn't work
lower = np.array([0, 0, 0], dtype='uint8')
upper = np.array([255, 255, 255], dtype='uint8')

def detect_skin(im):
	# resize the frame, convert it to the HSV color space,
	# and determine the HSV pixel intensities that fall into
	# the specified upper and lower boundaries
	converted = cvtColor(im, COLOR_BGR2HSV)
	skinMask = inRange(converted, lower, upper)
	
	min = [100,100,100]
	max = [100,100,100]
	for row in im:
		for col in row:
			for i in range(3):
				if col[i] < min[i]:
					min[i] = col[i]
				if col[i] > max[i]:
					max[i] = col[i]
	print min
	print max

	# apply a series of erosions and dilations to the mask
	# using an elliptical kernel
	#kernel = getStructuringElement(MORPH_ELLIPSE, (11, 11))
	#skinMask = erode(skinMask, kernel, iterations = 2)
	#skinMask = dilate(skinMask, kernel, iterations = 2)

	# blur the mask to help remove noise, then apply the
	# mask to the frame
	#skinMask = GaussianBlur(skinMask, (3, 3), 0)
	#skin = bitwise_and(im, im, mask=skinMask)
	
	return skinMask

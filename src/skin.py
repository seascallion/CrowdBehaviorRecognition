# import the necessary packages
import numpy as np
import cv2

def detect_skin(oImage):
    # define the upper and lower boundaries of the HSV pixel
    # intensities to be considered 'skin'
    lower = np.array([0, 48, 60], dtype='uint8')
    upper = np.array([20, 255, 255], dtype='uint8')

    # grab the image
    #imagePath = '../data/images/006.jpg'
    #oImage = cv2.imread(imagePath)
    image = cv2.resize(oImage, (0,0), fx=2, fy=2)

    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the specified upper and lower boundaries
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)

    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    skinMask = cv2.erode(skinMask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)

    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    #skin = cv2.bitwise_and(image, image, mask=skinMask)

    # show the skin in the image along with the mask
    #cv2.imshow('images', np.hstack([image, skin]))
    #cv2.waitKey(0)

    return skinMask

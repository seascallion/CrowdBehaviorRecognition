import cv2
from cv2 import imread, Sobel, CV_64F
import numpy as np
from skin import detect_skin
def analyze( im ):

    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.resize(im_gray, (1280, 720));

    ksize = 5

    sobel_x = np.abs(Sobel(im_gray, CV_64F, 1, 0, ksize=ksize))
    sobel_y = np.abs(Sobel(im_gray, CV_64F, 0, 1, ksize=ksize))

    sobel_x *= 255.0 / sobel_x.max()
    sobel_y *= 255.0 / sobel_y.max()

    skin = detect_skin(im)

    vert_amount = sobel_x.mean()
    horz_amount = sobel_y.mean()

    cheeringness = np.log(vert_amount / horz_amount)

    density = skin.mean() / skin.max()

    return (cheeringness, density)

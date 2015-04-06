from cv2 import Sobel, CV_64F
from math import atan2, pi


# Returns images representing magnitude and direction of image gradient.
# For now, assumes a grayscale image.
def gradient(im):

    ksize = 3

    sobel_x = Sobel(im, CV_64F, 1, 0, ksize=ksize)
    sobel_y = Sobel(im, CV_64F, 0, 1, ksize=ksize)

    mag = [
        [
            (grad_x**2 + grad_y**2)**0.5 for (grad_x, grad_y) in zip(row_x, row_y)
        ] for (row_x, row_y) in zip(sobel_x, sobel_y)
    ]
    ori = [
        [
            atan2(grad_y, grad_x) for (grad_x, grad_y) in zip(row_x, row_y)
        ] for (row_x, row_y) in zip(sobel_x, sobel_y)
    ]

    return mag, ori


# Returns a histogram of gradient orientations for an image, given a (grayscale) image.
def hog(im, precision=8):
    im_mag, im_ori = gradient(im)
    h, w = len(im), len(im[0])

    histogram = [0] * precision

    for angle in range(precision):
        for i in range(h):
            for j in range(w):
                mag = im_mag[i][j]
                ori = im_ori[i][j]
                ori_index = round(ori / (2 * pi) * precision)
                if ori_index == precision:
                    ori_index = 0
                    histogram[ori_index] += mag

    return histogram

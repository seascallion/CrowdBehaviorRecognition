from cv2 import imread, Sobel, CV_64F
from matplotlib.pyplot import title, xticks, yticks, subplot, imshow, show
from skin import detect_skin
import numpy as np

filename = '002.jpg'

directory = '../data/images'

im = imread(directory + '/' + filename)

subplot(221), imshow(im, cmap='gray')
title('Original Image'), xticks([]), yticks([])

ksize = 5

sobel_x = np.abs(Sobel(im, CV_64F, 1, 0, ksize=ksize))
sobel_y = np.abs(Sobel(im, CV_64F, 0, 1, ksize=ksize))

sobel_x *= 255.0 / sobel_x.max()
sobel_y *= 255.0 / sobel_y.max()

subplot(223), imshow(sobel_x, cmap='gray')
title('Sobel X'), xticks([]), yticks([])

subplot(224), imshow(sobel_y, cmap='gray')
title('Sobel Y'), xticks([]), yticks([])

skin = detect_skin(im)

subplot(222), imshow(skin, cmap='gray')
title('Skin'), xticks([]), yticks([])

vert_amount = sobel_x.mean()
horz_amount = sobel_y.mean()

cheeringness = np.log(vert_amount / horz_amount)

density = skin.mean() / skin.max()

print 'File:', filename
print 'Cheeringness:', cheeringness
print 'Density:', density

show()

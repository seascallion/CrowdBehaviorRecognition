from cv2 import *
from matplotlib.pyplot import *
from gradient import gradient

filename = 'crowd4.jpg'

directory = '../data/images'

im = imread(directory + '/' + filename)
im = cvtColor(im, COLOR_RGB2GRAY)

subplot(221), imshow(im, cmap='gray')
title('Original Image'), xticks([]), yticks([])

mag, ori = gradient(im)

subplot(223), imshow(mag, cmap='gray')
title('Gradient Magnitude'), xticks([]), yticks([])

subplot(224), imshow(ori, cmap='gray')
title('Gradient Orientation'), xticks([]), yticks([])

"""
vert_amount = sobel_x.mean()
horz_amount = sobel_y.mean()

cheeringness = np.log(vert_amount / horz_amount)

print 'File:', filename
print 'Cheeringness:', cheeringness
"""

show()

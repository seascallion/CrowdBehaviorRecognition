from cv2 import *
from matplotlib.pyplot import *

im = imread('../data/images/crowd.jpg')
edges = Canny(im, 100, 200)

subplot(121), imshow(im, cmap='gray')
title('Original Image'), xticks([]), yticks([])
subplot(122), imshow(edges, cmap='gray')
title('Edges'), xticks([]), yticks([])

show()

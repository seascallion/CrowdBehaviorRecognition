from cv2 import *
from matplotlib.pyplot import *


def mag_spec(im):
    # Fourier transform
    f = np.fft.fft2(im)
    fshift = np.fft.fftshift(f)
    result = np.log(np.abs(fshift))
    result *= 255.0 / result.max()
    return result

im = imread('../data/images/crowd4.jpg')
im = cvtColor(im, COLOR_RGB2GRAY)

subplot(221), imshow(im, cmap='gray')
title('Original Image'), xticks([]), yticks([])

# Canny edges
#edges = Canny(im, 200, 255)

#subplot(222), imshow(edges, cmap='gray')
#title('Magnitude Spectrum'), xticks([]), yticks([])

ksize = 5

sobel_x = np.abs(Sobel(im, CV_64F, 1, 0, ksize=ksize))
sobel_y = np.abs(Sobel(im, CV_64F, 0, 1, ksize=ksize))

sobel_x *= 255.0 / sobel_x.max()
sobel_y *= 255.0 / sobel_y.max()

#edge_mag_spec = mag_spec(edges)

subplot(223), imshow(sobel_x, cmap='gray')
title('Sobel X'), xticks([]), yticks([])

subplot(224), imshow(sobel_y, cmap='gray')
title('Sobel Y'), xticks([]), yticks([])

vert_amount = sobel_x.mean()
horz_amount = sobel_y.mean()

cheeringness = vert_amount / horz_amount

print 'Cheeringness:', cheeringness

show()

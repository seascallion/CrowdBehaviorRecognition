from cv2 import *
from matplotlib.pyplot import *

im = imread('../data/images/crowd.jpg')

subplot(241), imshow(im, cmap='gray')
title('Original Image'), xticks([]), yticks([])

# Canny edges
edges = Canny(im, 200, 255)
subplot(242), imshow(edges, cmap='gray')
title('Edges'), xticks([]), yticks([])

# Gabor segmentation
params = {
    'ksize': (100, 100),
    'sigma': 1.0,
    'theta': 3.14 / 2,
    'lambd': 15.0,
    'gamma': 0.02,
    #'psi': 0,
    'ktype': CV_32F
}
kern = getGaborKernel(**params)

result = filter2D(im, CV_8UC3, kern)

subplot(243), imshow(result, cmap='gray')
title('Segmented'), xticks([]), yticks([])

# Fourier transform
f = np.fft.fft2(edges)
fshift = np.fft.fftshift(f)
mag_spec = np.log(np.abs(fshift))
mag_spec *= 255.0 / mag_spec.max()

subplot(244), imshow(mag_spec, cmap='gray')
title('Magnitude Spectrum'), xticks([]), yticks([])

im = GaussianBlur(mag_spec, ksize=(301, 301), sigmaX=50, sigmaY=50, borderType=BORDER_REFLECT)
sobel_y = Sobel(im, CV_64F, 0, 1, ksize=31)

sobel_y *= 255.0 / sobel_y.max()

subplot(245), imshow(im, cmap='gray')
title('Blurred Result'), xticks([]), yticks([])

subplot(246), imshow(sobel_y, cmap='gray')
title('Sobel of That'), xticks([]), yticks([])

show()

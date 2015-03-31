from cv2 import *
from matplotlib.pyplot import *

im = imread('../data/images/crowd.jpg')

subplot(221), imshow(im, cmap='gray')
title('Original Image'), xticks([]), yticks([])

# Canny edges
edges = Canny(im, 200, 255)
subplot(222), imshow(edges, cmap='gray')
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

subplot(223), imshow(result, cmap='gray')
title('Segmented'), xticks([]), yticks([])

# Fourier transform
f = np.fft.fft2(im)
fshift = np.fft.fftshift(f)
mag_spec = np.log(np.abs(fshift))
mag_spec *= 255.0 / mag_spec.max()

subplot(224), imshow(mag_spec, cmap='gray')
title('Magnitude Spectrum'), xticks([]), yticks([])

show()

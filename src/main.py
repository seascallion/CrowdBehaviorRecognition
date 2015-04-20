from cv2 import imread, Sobel, CV_64F
from matplotlib.pyplot import title, xticks, yticks, subplot, imshow, show
from skin import detect_skin
import numpy as np

filenames = [
    '000.jpg',
    '001.jpg',
    '002.jpg',
    '003.jpg',
    '004.jpg',
    '005.jpg',
    '006.jpg',
    '007.jpg',
    '008.jpg',
    '009.jpg',
    '010.jpg',
    '011.jpg',
    '012.jpg',
    '013.png',
    '014.jpg',
    '015.jpg',
    '016.jpg',
    '017.jpg',
    '018.jpg',
    '019.jpg',
    '020.jpeg',
    '021.jpg',
    '022.jpg',
    '023.jpg',
    '024.jpg',
    '025.jpg',
    '026.jpg',
    '027.jpg',
    '028.jpg',
    '029.jpg',
    '030.jpg',
    '031.jpg',
    '032.jpg',
    '033.jpg',
    '034.jpg',
    '035.jpg',
    '036.jpg',
    '037.jpg',
    '038.jpg',
    '039.jpg',
    '040.jpg',
    '041.jpg',
    '042.jpg',
    '043.jpg'
]

display_filename = '043.jpg'

directory = '../data/images'

for filename in filenames:

    im = imread(directory + '/' + filename)

    ksize = 5

    sobel_x = np.abs(Sobel(im, CV_64F, 1, 0, ksize=ksize))
    sobel_y = np.abs(Sobel(im, CV_64F, 0, 1, ksize=ksize))

    sobel_x *= 255.0 / sobel_x.max()
    sobel_y *= 255.0 / sobel_y.max()

    skin = detect_skin(im)

    vert_amount = sobel_x.mean()
    horz_amount = sobel_y.mean()

    cheeringness = np.log(vert_amount / horz_amount)

    density = skin.mean() / skin.max()

    print 'File:', filename
    print 'Cheeringness: %.4f' % cheeringness
    print 'Density: %.4f' % density
    print ''

    if filename == display_filename:
        subplot(221), imshow(im, cmap='gray')
        title('Original Image'), xticks([]), yticks([])

        subplot(223), imshow(sobel_x, cmap='gray')
        title('Sobel X'), xticks([]), yticks([])

        subplot(224), imshow(sobel_y, cmap='gray')
        title('Sobel Y'), xticks([]), yticks([])

        subplot(222), imshow(skin, cmap='gray')
        title('Skin'), xticks([]), yticks([])

        show()

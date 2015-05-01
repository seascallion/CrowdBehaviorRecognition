from sys import argv
import os
from PIL import Image


def crop(infile, height, width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

if __name__ == '__main__':
    infile = argv[1]
    width = int(argv[2])
    height = int(argv[3])
    outpath = argv[4]
    for k, piece in enumerate(crop(infile, height, width)):
        img = Image.new('RGBA', (height, width), 255)
        img.paste(piece)
        if img.getpixel((1, 1))[-1] == 0:
            break
        path = os.path.join(outpath, '%04d.png' % k)
        img.save(path)

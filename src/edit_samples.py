#! /usr/bin/env python
import argparse
import cv2
import os
import ntpath

# use Unix-style separators (works on both Unix and Windows)
os.sep = '/'

# initialize the list of reference points
refPt = []

pos_data = {}
neg_data = {}

im_drag = None

dragging_pos = False
dragging_neg = False

path_rel = ''


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, dragging_pos, dragging_neg, im_drag

    height, width, depth = image.shape

    # Left mouse button down -> start positive drag sample
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        dragging_pos = True

    # Right mouse button down -> start negative drag sample
    elif event == cv2.EVENT_RBUTTONDOWN:
        refPt = [(x, y)]
        dragging_neg = True

    # Mouse move -> update drag sample
    elif event == cv2.EVENT_MOUSEMOVE:
        mag_size = 64
        mag_factor = 4
        mx = mag_size / 2 if x < mag_size / 2 else width - mag_size / 2 - 1 if x >= width - mag_size / 2 else x
        my = mag_size / 2 if y < mag_size / 2 else height - mag_size / 2 - 1 if y >= height - mag_size / 2 else y
        offset_x = x - mx
        offset_y = y - my
        viewing_image = im_drag if im_drag is not None else image
        magnified_image = cv2.resize(viewing_image[(my - mag_size / 2):(my + mag_size / 2), (mx - mag_size / 2):(mx + mag_size / 2)], (0, 0), fx=mag_factor, fy=mag_factor)
        cv2.rectangle(magnified_image, ((mag_size / 2 + offset_x - 4) * mag_factor, (mag_size / 2 + offset_y - 4) * mag_factor), ((mag_size / 2 + offset_x + 4) * mag_factor, (mag_size / 2 + offset_y + 4) * mag_factor), (255, 255, 255), mag_factor / 2)
        cv2.imshow('Magnifier', magnified_image)
        if dragging_pos or dragging_neg:
            im_drag = image.copy()
            size = min(max(4, abs(x - refPt[0][0]), abs(y - refPt[0][1])), refPt[0][0], refPt[0][1], width - refPt[0][0] - 1, height - refPt[0][1] - 1)
            if dragging_pos:
                cv2.rectangle(im_drag, (refPt[0][0] - size, refPt[0][1] - size), (refPt[0][0] + size, refPt[0][1] + size), (127, 255, 127), 1)
            if dragging_neg:
                cv2.rectangle(im_drag, (refPt[0][0] - size, refPt[0][1] - size), (refPt[0][0] + size, refPt[0][1] + size), (255, 127, 255), 1)

    # Left mouse button up -> stop positive drag sample
    elif event == cv2.EVENT_LBUTTONUP:
        im_drag = None
        refPt.append((x, y))
        dragging_pos = False
        size = min(max(4, abs(refPt[1][0] - refPt[0][0]), abs(refPt[1][1] - refPt[0][1])), refPt[0][0], refPt[0][1], width - refPt[0][0] - 1, height - refPt[0][1] - 1)
        new_rect = (refPt[0][0] - size, refPt[0][1] - size, size * 2, size * 2)
        pos_data[path_rel].append(new_rect)
        cv2.rectangle(image, (new_rect[0], new_rect[1]), (new_rect[0] + new_rect[2], new_rect[1] + new_rect[3]), (0, 255, 0), 1)
        cv2.imshow('image', image)

    # Right mouse button up -> stop negative drag sample
    elif event == cv2.EVENT_RBUTTONUP:
        im_drag = None
        refPt.append((x, y))
        dragging_neg = False
        size = min(max(4, abs(refPt[1][0] - refPt[0][0]), abs(refPt[1][1] - refPt[0][1])), refPt[0][0], refPt[0][1], width - refPt[0][0] - 1, height - refPt[0][1] - 1)
        new_rect = (refPt[0][0] - size, refPt[0][1] - size, size * 2, size * 2)
        neg_data[path_rel].append(new_rect)
        cv2.rectangle(image, (new_rect[0], new_rect[1]), (new_rect[0] + new_rect[2], new_rect[1] + new_rect[3]), (255, 0, 255), 1)
        cv2.imshow('image', image)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', default='../data/images/hand_sampleImages', help='Path to the images folder')
ap.add_argument('-o', '--output', default='../data/images/hand_classifier', help='Path to the output folder for data files')
args = vars(ap.parse_args())

images_path = args['images'].replace('\\', os.sep)
output_path = args['output'].replace('\\', os.sep)
positive_path = os.sep.join([output_path, 'positive.dat'])
negative_path = os.sep.join([output_path, 'negative.dat'])
bg_path = os.sep.join([output_path, 'bg.dat'])

# Ensure output path exists
if not os.path.exists(output_path):
    os.makedirs(output_path)

image_paths = sorted([
    os.sep.join([images_path, filename])
    for filename in os.listdir(images_path)
    if any(filename.endswith('.{0}'.format(ext)) for ext in ['jpg', 'jpeg', 'png'])
])


# load description data
with open(positive_path, 'a+') as output_file:
    for line in output_file.readlines():
        tokens = line.split()
        img_path = tokens[0]
        rect_count = int(tokens[1])
        rects = [tuple(int(x) for x in rect) for rect in chunks(tokens[2:], 4)]
        assert(len(rects) == rect_count)
        pos_data[img_path] = rects
with open(negative_path, 'a+') as output_file:
    for line in output_file.readlines():
        tokens = line.split()
        img_path = tokens[0]
        rect_count = int(tokens[1])
        rects = [tuple(int(x) for x in rect) for rect in chunks(tokens[2:], 4)]
        assert(len(rects) == rect_count)
        neg_data[img_path] = rects


image_index = 0

done = False

while not done:
    image_path = image_paths[image_index]
    path_rel = os.path.relpath(image_path, output_path).replace('\\', os.sep)
    if path_rel not in pos_data:
        pos_data[path_rel] = []
    if path_rel not in neg_data:
        neg_data[path_rel] = []

    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(image_path)

    clone = image.copy()
    for rect in pos_data[path_rel]:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
    for rect in neg_data[path_rel]:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 255), 1)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', click_and_crop)

    while True:
        # display the image and wait for a keypress
        cv2.imshow('image', im_drag if im_drag is not None else image)
        key = cv2.waitKey(1)

        # if the 'r' key is pressed, reset the regions
        if key == 114:
            image = clone.copy()
            pos_data[path_rel] = []
            neg_data[path_rel] = []

        # if the left or up key is pressed, go down an image
        elif key in (2424832, 2490368):
            image_index = (image_index - 1) % len(image_paths)
            break

        # if the right or down or enter or space key is pressed, go up an image
        elif key in (2555904, 2621440, 13, 32):
            image_index = (image_index + 1) % len(image_paths)
            break

        # if escape key is pressed, save and exit
        elif key == 27:
            done = True
            break

# save description data
with open(positive_path, 'w+') as output_file:
    for filename, rects in pos_data.items():
        if len(rects) > 0:
            line = filename + ' ' + str(len(rects)) + ' ' + ' '.join(' '.join(str(x) for x in rect) for rect in rects)
            output_file.write('%s\n' % line)
with open(negative_path, 'w+') as output_file:
    for filename, rects in neg_data.items():
        if len(rects) > 0:
            line = filename + ' ' + str(len(rects)) + ' ' + ' '.join(' '.join(str(x) for x in rect) for rect in rects)
            output_file.write('%s\n' % line)

# crop negative samples into their own files. OpenCV training system needs it done this way. Supes complicated, I know
negative_samples_path = os.path.join(output_path, 'bg')
if not os.path.exists(negative_samples_path):
    os.makedirs(negative_samples_path)
index = 0
for filename in os.listdir(negative_samples_path):
    filepath = os.path.join(negative_samples_path, filename)
    if os.path.isfile(filepath):
        os.unlink(filepath)
with open(bg_path, 'w+') as output_file:
    for filename, rects in neg_data.items():
        filepath = os.path.join(images_path, filename)
        image = cv2.imread(filepath)
        for rect in rects:
            cropped_image = image[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
            cropped_filename = '%04d.jpg' % index
            cropped_filepath = os.path.join(negative_samples_path, cropped_filename)
            cv2.imwrite(cropped_filepath, cropped_image)
            index += 1
            rel_cropped_filename = os.path.relpath(cropped_filepath, output_path).replace('\\', os.sep)
            output_file.write('%s\n' % rel_cropped_filename)

# close all open windows
cv2.destroyAllWindows()

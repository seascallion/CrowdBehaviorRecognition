#!/usr/bin/env python

import cv2
from sys import argv
import os


cascade_names = [
    #'haarcascade_upperbody',
    #'haarcascade_frontalface_default',
    #'haarcascade_frontalface_alt',
    #'haarcascade_frontalface_alt2',
    #'haarcascade_frontalface_alt_tree',
    #'haarcascade_fullbody',
    #'haarcascade_mcs_upperbody',
    #'haarcascade_profileface',
    'haarcascade_smile',
]
classifiers = {
    cascade_name: cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/%s.xml' % cascade_name)
    for cascade_name in cascade_names
}
filenames = argv[1:] if len(argv) > 1 else os.listdir('../data/images')

face_classifier_names = [
    'haarcascade_frontalface_default',
    'haarcascade_frontalface_alt',
    'haarcascade_frontalface_alt2',
    'haarcascade_frontalface_alt_tree',
    'haarcascade_profileface',
]

face_classifiers = {
    classifier_name: cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/%s.xml' % classifier_name)
    for classifier_name in face_classifier_names
}
smile_classifier = cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/%s.xml' % 'haarcascade_smile')

for filename in filenames:
    image = cv2.imread('../data/images/%s' % filename)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    width, height = image_gray.shape
    print filename, '%dx%d' % (width, height)
    faces = []
    for classifier_name, face_classifier in face_classifiers.items():
        faces = list(face_classifier.detectMultiScale(image_gray, 1.1, 4))
        print '\t{0}: {1}'.format(classifier_name, len(faces))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            face = image_gray[y:y + h, x:x + w]
            smiles = smile_classifier.detectMultiScale(face, 1.1, 3)
            if len(smiles):
                print '\t\t{0} smile{1} detected'.format(len(smiles), 's' if len(smiles) > 1 else '')
            for (x_, y_, w_, h_) in smiles:
                cv2.rectangle(image, (x + x_, y + y_), (x + x_ + w_, y + y_ + h_), (255, 0, 255), 1)


    cv2.imshow('image', image)
    cv2.moveWindow('image', 0, 0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
for filename in filenames:
    image = cv2.imread('../data/images/%s' % filename)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print filename, '%dx%d' % image_gray.shape
    for classifier_name, classifier in classifiers.items():
        objects = classifier.detectMultiScale(image_gray, 1.1, 1)
        print '    ', classifier_name, ':', len(objects)
        for (x, y, w, h) in objects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('image', image)
    cv2.moveWindow('image', 0, 0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""

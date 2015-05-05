import cv2
import csv
from cv2 import imread, Sobel, CV_64F
from matplotlib.pyplot import title, xticks, yticks, subplot, imshow, show
from analysis import analyze
import numpy as np
from os import listdir

display_filenames = []
test_results = dict()

cheer_threshold = 0.05
density_low_threshold = 0.1
density_high_threshold = 0.18

directory = '../data/images/sampleImages'
with open('../data/csv.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        test_filename = row['file']
        test_results[test_filename] = row

density_dict = {
    'low': [0, 0],
    'medium': [0, 0],
    'high': [0, 0]
}

cheering_dict = {
    'idle': [0, 0],
    'cheering': [0, 0]
}

for filename in sorted(listdir(directory)):

    im = imread(directory + '/' + filename)
    cheeringness, density, sobel_x, sobel_y, skin = analyze(im, True)

    cheering_s = 'cheering' if cheeringness > cheer_threshold else 'idle'
    density_s = 'low' if density < density_low_threshold else ('medium' if density < density_high_threshold else 'high')

    shortFilename = filename.split('.')[0]
    true_density = test_results[shortFilename]['density']
    if density_s == true_density:
        density_dict[true_density][0] += 1
    else:
        density_dict[true_density][1] += 1

    true_cheer = test_results[shortFilename]['action']
    if cheering_s == true_cheer:
        cheering_dict[true_cheer][0] += 1
    else:
        cheering_dict[true_cheer][1] += 1

    # Delete this sectoin latetr
    #if true_density == 'high' and density_s != true_density:
       #display_filenames.append(filename)

    print 'File:', filename
    print 'Cheeringness: ',cheering_s, ' ', test_results[shortFilename]['action'],cheeringness
    print 'Density:',density_s, ' ', true_density, density
    print ''

    if filename in display_filenames:
        subplot(221), imshow(im, cmap='gray')
        title('Original Image'), xticks([]), yticks([])

        subplot(223), imshow(sobel_x, cmap='gray')
        title('Sobel X'), xticks([]), yticks([])

        subplot(224), imshow(sobel_y, cmap='gray')
        title('Sobel Y'), xticks([]), yticks([])

        subplot(222), imshow(skin, cmap='gray')
        title('Skin'), xticks([]), yticks([])

        show()

high_total = sum(density_dict['high'])
medium_total = sum(density_dict['medium'])
low_total = sum(density_dict['low'])

high_correct = density_dict['high'][0]
medium_correct = density_dict['medium'][0]
low_correct = density_dict['low'][0]

high_percent = (1.0*high_correct)/(1.0*high_total) * 100.0
medium_percent = (1.0*medium_correct)/(1.0*medium_total) * 100.0
low_percent = (1.0*low_correct)/(1.0*low_total) * 100.0

print 'High Density:', high_correct,'of',high_total,'(%.2f%%' % high_percent,')'
print 'Medium Density ', medium_correct,'of',medium_total,'(%.2f%%' % medium_percent,')'
print 'Low Density:', low_correct,'of',low_total,'(%.2f%%' % low_percent,')'


idle_total = sum(cheering_dict['idle'])
cheering_total = sum(cheering_dict['cheering'])

idle_correct = cheering_dict['idle'][0]
cheering_correct = cheering_dict['cheering'][0]

idle_percent = (1.0*idle_correct)/(1.0*idle_total) * 100.0
cheering_percent = (1.0*cheering_correct)/(1.0*cheering_total) * 100.0

print ' '
print 'Idle Activity', idle_correct,'of',idle_total,'(%.2f%%' % idle_percent,')'
print 'Cheering Activity', cheering_correct,'of',cheering_total,'(%.2f%%' % cheering_percent,')'

#! /usr/bin/env python

import cv2
import csv
from matplotlib import pyplot as plt
from analysis import analyze
import numpy as np
import os

display_filenames = ['002.jpg']
test_results = dict()

cheer_threshold = 0.05
density_threshold = 0.08

directory = '../data/images/categorized'

already_displayed_filenames = set()

confusion_dicts = {}

# Dictionary of data per image filename.
image_data = {}

for root, dirs, files in os.walk(directory):
	
	for filename in files:
		file_path = os.path.join(root, filename)
		
		path_split = root.split(os.sep)
		parameter = path_split[-2]
		true_value = path_split[-1]
		
		# Predict the value of the density
		if parameter == 'density':
			if filename not in image_data:
				im = cv2.imread(file_path)
				image_data[filename] = analyze(im, True)
			cheeringness, density, sobel_x, sobel_y, skin = image_data[filename]
			predicted_value = 'sparse' if density < density_threshold else 'dense'
		# Predict the state of the activity
		elif parameter == 'activity':
			if filename not in image_data:
				im = cv2.imread(file_path)
				image_data[filename] = analyze(im, True)
			cheeringness, density, sobel_x, sobel_y, skin = image_data[filename]
			predicted_value = 'cheering' if cheeringness > cheer_threshold else 'idle'
		else:
			continue
		
		# Increment the count in the confusion matrices.
		if parameter not in confusion_dicts:
			confusion_dicts[parameter] = {}
		if true_value not in confusion_dicts[parameter]:
			confusion_dicts[parameter][true_value] = {}
		if predicted_value not in confusion_dicts[parameter][true_value]:
			confusion_dicts[parameter][true_value][predicted_value] = 0
		confusion_dicts[parameter][true_value][predicted_value] += 1
		
		# Display the image in a window if we set it to.
		if filename in display_filenames and filename not in already_displayed_filenames:
			already_displayed_filenames.add(filename)
			
			plt.subplot(221), plt.imshow(im, cmap='gray')
			plt.title('Original Image'), plt.xticks([]), plt.yticks([])

			plt.subplot(223), plt.imshow(sobel_x, cmap='gray')
			plt.title('Sobel X'), plt.xticks([]), plt.yticks([])

			plt.subplot(224), plt.imshow(sobel_y, cmap='gray')
			plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

			plt.subplot(222), plt.imshow(skin, cmap='gray')
			plt.title('Skin'), plt.xticks([]), plt.yticks([])

			plt.show()

# Show the raw data for each image
minCheer = 99999.9
maxCheer = 0
minDense = 9999.9
maxDense = 0
for filename, data in image_data.items():
	print 'File:', filename
	print ' Cheeringness: %0.4f' % data[0]
	print ' Density:      %0.4f' % data[1]
	print ''

        if data[0] < minCheer:
            minCheer = data[0]
        if data[0] > maxCheer:
            maxCheer = data[0]
        if data[1] < minDense:
            minDense = data[1]
        if data[1] > maxDense:
            maxDense = data[1]
print minCheer,maxCheer,minDense,maxDense

# Show the confusion matrices with accuracy proportions
for parameter, confusion_dict in confusion_dicts.items():
	values = sorted(confusion_dict.keys())
	print 'Confusion matrix for %s:' % parameter
	print ''
	print '               PREDICTED'
	print 'KNOWN     | ' + ''.join(value.ljust(10) for value in values)
	print '-' * 10 + '-' + '-' * 10 * len(values)
	for value in values:
		predicted = confusion_dict[value]
		counts = [predicted[val] if val in predicted else 0 for val in values]
		total_count = sum(counts)
		proportions = [1.0 * count / total_count for count in counts]
		print value.ljust(10) + '|' + ''.join(('%0.2f' % prop).ljust(10) for prop in proportions)
	print ''
	total = sum(sum(prediction_vec.values()) for prediction_vec in confusion_dict.values())
	total_correct = sum(confusion_dict[value][value] for value in confusion_dict.keys())
	accuracy = 1.0 * total_correct / total
	print '* Average Accuracy is %0.2f' % accuracy
	print ''

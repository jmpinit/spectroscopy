#!/usr/bin/env python

import sys, os.path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pylab

# sum rows of image
def horiz_histogram(img):
	if(len(img.shape) == 2):
		height, width = img.shape
	else:
		height, width, channels = img.shape

	histogram = []
	for y in range(0, height):
		total = 0
		for x in range(0, width):
			total +=  np.mean(img[y, x].astype('int32'))
			
		histogram += [total] 

	return histogram

# change axis scale from pixel to wavelength
def pixel_to_wavelength(intensity, coeffs):
	return np.linspace(0, len(intensity)*coeffs[0], len(intensity))

# get the horizontal line with the brightest pixels
def best_line(img):
	best_pos = np.argmax(horiz_histogram(img))
	return img[best_pos]

# get intensity data by cropping to image after slit
def after_slit(img):
	imgline = best_line(img)
	
	if len(imgline.shape) > 1:
		intensity = np.mean(imgline, len(imgline.shape)-1)
	else:
		intensity = imgline

	return imgline[np.argmax(intensity):]

# turn image into spectrograph data
def converted(img, coeffs):
	# get pixel intensities
	y = after_slit(img)

	# use calibration to convert x axis from pixels to wavelength in nanometers
	x = pixel_to_wavelength(y, coeffs) + coeffs[1]

	return (x, y)

if __name__ == "__main__":
	# CLI arguments

	# ensure correct number of arguments
	if not len(sys.argv) == 4:
		print "usage: calibrate.py \"calibration image\" scale shift"
		sys.exit(1)

	image_filename = sys.argv[1]

	try:
		coeffs = [float(sys.argv[2]), float(sys.argv[3])]
	except ValueError:
		print "invalid scale or shift"
		print "must be floating point numbers"
		sys.exit(1)

	# ensure image exists
	if not os.path.isfile(image_filename):
		print "image file doesn't exist!"
		sys.exit(1)

	# analyze
	imgdata = cv2.imread("../data/processed/fluorescent.png", 0)

	# graph
	x, y = converted(imgdata, coeffs)
	plt.plot(x, y)
	plt.show()

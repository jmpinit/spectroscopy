#!/usr/bin/env python

import sys, os.path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import spectrograph

SPECTRUM_FLUORESCENT = [436, 542, 611]

if __name__ == "__main__":
	# CLI arguments

	# ensure correct number of arguments
	if not len(sys.argv) == 2:
		print "usage: calibrate.py \"calibration image\""
		sys.exit(1)

	image_filename = sys.argv[1]

	# ensure image exists
	if not os.path.isfile(image_filename):
		print "image file doesn't exist!"
		sys.exit(1)

	colordata = cv2.imread(image_filename, 1)

	# find best horizontal line
	intensity = spectrograph.after_slit(colordata)

	# separate the color channels
	blue = intensity[:,0]
	green = intensity[:,1]
	red = intensity[:,2]

	# find highest peak in each color channel
	# exclude the slit spike at origin
	red_px = np.argmax(red[100:])+100
	blue_px = np.argmax(blue[100:])+100
	green_px = np.argmax(green[100:])+100

	# calculate the calibration coefficients from the known fluorescent spectrum
	pixels = [blue_px, green_px, red_px]

	fit = np.polyfit(pixels, SPECTRUM_FLUORESCENT, 1)
	fit_fn = np.poly1d(fit)

	# output result
	print ''.join([str(v) + ' ' for v in fit_fn.c])

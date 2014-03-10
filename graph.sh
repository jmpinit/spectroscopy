#!/bin/bash

if [ "$#" -ne 2 ]
then
	echo "usage: graph.sh \"calibration image\" \"spectrograph image\""
else
	./spectrograph.py $2 $(./calibrate.py $1)
fi

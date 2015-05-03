#!/usr/bin/env bash
python src/split_image.py data/images/hands/all/positive.png 8 8 data/images/hands/positive
python src/split_image.py data/images/hands/all/negative.png 8 8 data/images/hands/negative

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from functools import reduce
from operator import add

from PIL import Image
from sense_hat import SenseHat

sense = SenseHat()

# Load image
# pixelart.png is a symlink to the actual image
image = Image.open("pixelart.png")

# Resize to 8x8 pixels
image = image.resize((8, 8))

# Create an empty 8x8 matrix
color = [0, 0, 0]
rgb_matrix = [[color for _ in range(8)] for _ in range(8)]

# Parse image and fill matrix
for y in range(8):
    for x in range(8):
        r, g, b, u = image.getpixel((x, y))
        rgb_matrix[y][x] = [r, g, b]

# Flatten matrix to a single list of colors
rgb_matrix = reduce(add, rgb_matrix)

# Send matrix to Sense HAT to validate the image
sense.set_pixels(rgb_matrix)

# Print matrix
# print(rgb_matrix)

# Compose JSON data
# Run the script and redirect the output to a file
# python3 pixelart.py > yoda.json
json_data = json.dumps({"leds": rgb_matrix})
print(json_data)

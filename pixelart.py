#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from sense_hat import SenseHat

sense = SenseHat()

# Charger l'image
image = Image.open("pixelart.png")

# Redimensionner à 8x8 pixels
image = image.resize((8, 8))

# Créer une matrice 8x8 vide
color = [0, 0, 0]
matrice_rgb = [[color for _ in range(8)] for _ in range(8)]

# Parcourir les pixels et remplir la matrice
for y in range(8):
    for x in range(8):
        r, g, b, u = image.getpixel((x, y))
        matrice_rgb[y][x] = [r, g, b]

# Afficher la matrice
for ligne in matrice_rgb:
    print(ligne)

sense.set_pixels(sum(matrice_rgb, []))

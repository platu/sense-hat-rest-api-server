#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from multipledispatch import dispatch
from sense_hat import SenseHat


sense = SenseHat()


# ----------------------------------------------------------------------------
# Send message to the led matrix display
# 3 different cases:
# 1. Only a string message
# 2. A string message and a speed
# 3. A string message, a speed, a foreground color and a background color
@dispatch(str)
def post_message(msg):
    sense.show_message(msg)


@dispatch(str, float)
def post_message(msg, speed):  # noqa F811
    fg_color = [255, 255, 255]
    bg_color = [0, 0, 0]
    sense.show_message(msg, speed, fg_color, bg_color)


@dispatch(str, float, list, list)
def post_message(msg, speed, fg_color, bg_color):  # noqa F811
    sense.show_message(msg, speed, fg_color, bg_color)


# ----------------------------------------------------------------------------
# Manage the led matrix display as a whole
# Clear the led matrix display with 2 different cases:
# 1. No arguments
# 2. A color to fill the led matrix display
@dispatch()
def clear_leds():
    sense.clear()


@dispatch(list)
def clear_leds(color):  # noqa F811
    sense.clear(color)


# Read all leds at once
def read_leds():
    return sense.get_pixels()


# Set all leds at once
def set_leds(leds):
    sense.set_pixels(leds)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


from multipledispatch import dispatch
from sense_hat import SenseHat


sense = SenseHat()


@dispatch(str)
def post_message(msg):
    sense.show_message(msg)


@dispatch(str, str)
def post_message(msg, speed):  # noqa F811
    speed = json.loads(speed)
    fg_color = [255, 255, 255]
    bg_color = [0, 0, 0]
    sense.show_message(msg, speed, fg_color, bg_color)


@dispatch(str, str, str, str)
def post_message(msg, speed, fg, bg):  # noqa F811
    speed = json.loads(speed)
    fg_color = json.loads(fg)
    bg_color = json.loads(bg)
    sense.show_message(msg, speed, fg_color, bg_color)


def read_leds():
    return json.dumps(sense.get_pixels(), indent=2)


def set_leds(leds):
    display = json.loads(leds)
    sense.set_pixels(display)

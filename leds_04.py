#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sense_hat import SenseHat

sense = SenseHat()


def post_message(msg):
    sense.show_message(msg)

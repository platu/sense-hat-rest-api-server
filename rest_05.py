#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect, request

import leds_04 as leds
import sensors_04 as sensors

app = Flask(__name__)


# ----------------------------------------------------------------------------
# Main index route
@app.route("/")
def index():
    return redirect("/api/v1", code=302)


@app.route("/api/v1", methods=["get"], strict_slashes=False)
def main():
    main_data = ["sensors", "leds", "messages"]
    return json.dumps(main_data, indent=2)


# ----------------------------------------------------------------------------
# Routes for the sensors
# 1. Get all sensors data
@app.route("/api/v1/sensors", methods=["get"], strict_slashes=False)
def route_sensors():
    return sensors.get_sensors_data()


# 2. Get a specific sensor data
@app.route("/api/v1/sensors/<name>", methods=["get"], strict_slashes=False)
def route_sensors_name(name):
    return sensors.get_sensors_data(name)


# ----------------------------------------------------------------------------
# Private function to validate a color list [r, g, b]
# Return a tuple with a boolean and an error message
# This function is used by many routes
def _isColorValid(color):
    try:
        for c in color:
            if (c < 0) or (c > 255):
                return False, "Invalid color value"
        return True
    except TypeError:
        return False, "Invalid color type"


# ----------------------------------------------------------------------------
# Route for the messages
@app.route("/api/v1/messages/", methods=["post"], strict_slashes=False)
def route_messages():
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON"},
                          indent=2), 400
    if "msg" not in data:
        return json.dumps({"error": "Missing 'msg' key"},
                          indent=2), 400
    else:
        msg = data["msg"]
        if "speed" in data:
            try:
                speed = float(data["speed"])
            except ValueError:
                return json.dumps({"error": "Invalid speed value"},
                                  indent=2), 400
        else:
            # Back to default speed
            speed = 0.1
        if "fg" in data and "bg" in data:
            fg = json.loads(data["fg"])
            bg = json.loads(data["bg"])
            fg_valid, fg_error = _isColorValid(fg)
            bg_valid, bg_error = _isColorValid(bg)
            if not fg_valid:
                return json.dumps({"error": fg_error},
                                  indent=2), 400
            if not bg_valid:
                return json.dumps({"error": bg_error},
                                  indent=2), 400
            # Scroll message with speed, foreground and background colors
            leds.post_message(msg, speed, fg, bg)
        else:
            # Scroll message with or without speed
            leds.post_message(msg, speed)
    return json.dumps({"message": "Message processed"}, indent=2)


@app.route("/api/v1/leds", methods=["get"], strict_slashes=False)
def route_read_leds():
    return leds.read_leds()


@app.route("/api/v1/leds", methods=["delete"], strict_slashes=False)
def route_clear_leds():
    if request.data:
        try:
            data = request.get_json()
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON"},
                              indent=2), 400
        if "color" in data:
            rgb = json.loads(data["color"])
            rgb_valid, rgb_error = _isColorValid(rgb)
            if not rgb_valid:
                return json.dumps({"error": rgb_error},
                                  indent=2), 400
            else:
                leds.clear_leds(rgb)
    else:
        leds.clear_leds()
    return json.dumps({"message": "LEDs cleared"}, indent=2)


@app.route("/api/v1/leds", methods=["post"], strict_slashes=False)
def route_set_leds():
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON"}, indent=2), 400
    if "leds" not in data:
        return json.dumps({"error": "Missing 'leds' key"}, indent=2), 400
    else:
        matrix = json.loads(data["leds"])
        print(matrix)
        if len(matrix) != 64:
            return json.dumps({"error": "Invalid matrix size"}, indent=2), 400
        else:
            leds.set_leds(matrix)
    return json.dumps({"message": "LEDs processed"}, indent=2)


if __name__ == "__main__":
    app.run(debug=True, host="::", port=8080)  # nosec

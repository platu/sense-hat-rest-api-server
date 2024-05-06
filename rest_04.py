#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect, request

import leds_04 as leds
import sensors_04 as sensors

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/api/v1", code=302)


@app.route("/api/v1", methods=["get"], strict_slashes=False)
def main():
    main_data = ["sensors", "leds", "messages"]
    return json.dumps(main_data, indent=2)


@app.route("/api/v1/sensors", methods=["get"], strict_slashes=False)
def route_sensors():
    return sensors.get_sensors_data()


@app.route("/api/v1/sensors/<name>", methods=["get"], strict_slashes=False)
def route_sensors_name(name):
    return sensors.get_sensors_data(name)


@app.route("/api/v1/messages/", methods=["post"], strict_slashes=False)
def route_messages():
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON"}, indent=2), 400
    if "msg" not in data:
        return json.dumps({"error": "Missing 'msg' key"}, indent=2), 400
    else:
        msg = data["msg"]
        if "speed" in data:
            speed = data["speed"]
        else:
            speed = "0.1"
        if "fg" in data and "bg" in data:
            fg = data["fg"]
            bg = data["bg"]
            leds.post_message(msg, speed, fg, bg)
        else:
            leds.post_message(msg, speed)
    return json.dumps({"message": "Message processed"}, indent=2)


@app.route("/api/v1/leds", methods=["get"], strict_slashes=False)
def route_read_leds():
    return leds.read_leds()


@app.route("api/v1/leds", methods=["post"], strict_slashes=False)
def route_set_leds():
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON"}, indent=2), 400
    if "leds" not in data:
        return json.dumps({"error": "Missing 'leds' key"}, indent=2), 400
    else:
        leds.set_leds(data["leds"])
    return json.dumps({"message": "LEDs processed"}, indent=2)


if __name__ == "__main__":
    app.run(debug=True, host="::", port=8080)  # nosec

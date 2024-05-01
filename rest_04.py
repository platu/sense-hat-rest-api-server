#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect, request

import sensors_04 as sensors
import leds_04 as leds

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
        leds.post_message(msg)
    return json.dumps({"message": "Message processed"}, indent=2)


if __name__ == "__main__":
    app.run(debug=True, host="::", port=8080)  # nosec

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect

import sensors_02 as sensors

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/api/v1", code=302)


@app.route("/api/v1", methods=["get"], strict_slashes=False)
def main():
    main_data = ["sensors", "leds", "messages"]
    return json.dumps(main_data, indent=2)


@app.route("/api/v1/sensors", methods=["get"], strict_slashes=False)
def sensors_route():
    return sensors.get_sensors_data()


if __name__ == "__main__":
    app.run(debug=True, host="::", port=8080)  # nosec

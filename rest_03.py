#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, redirect
import json
import sensors_03 as sensors

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/api/v1', code=302)


@app.route('/api/v1', methods=["get"])
def main():
    main_data = ["sensors", "leds", "messages"]
    return json.dumps(main_data, indent=2)


@app.route('/api/v1/sensors', methods=["get"])
def route_sensors():
    return sensors.get_sensors_data()


@app.route('/api/v1/sensors/<name>', methods=["get"])
def route_sensors_name(name):
    return sensors.get_sensors_data(name)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

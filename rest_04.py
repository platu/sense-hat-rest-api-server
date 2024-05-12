#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect, request

import leds_04 as leds
import sensors_04 as sensors


def create_app():
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
    # Private function to validate JSON
    def _isValidJSON(data):
        try:
            json.loads(data)
        except json.JSONDecodeError:
            return False
        return True

    # ----------------------------------------------------------------------------
    # Private function to validate a color list [r, g, b]
    # Return a tuple with a boolean and an error message
    # This function is used by many routes
    def _isValidColor(color):
        for c in color:
            if (c < 0) or (c > 255):
                return False
        return True

    # ----------------------------------------------------------------------------
    # Route for the messages
    @app.route("/api/v1/messages/", methods=["post"], strict_slashes=False)
    def route_messages():
        msg = speed = fg = bg = None
        if _isValidJSON(request.data) is False:
            return json.dumps(
                {"error": "Invalid JSON"}
            ), 400
        else:
            data = request.get_json()
        if data.get("msg") is None:
            return json.dumps(
                {"error": "Missing 'msg' key"}
            ), 400
        else:
            msg = data["msg"]
        if data.get("speed") is not None:
            try:
                speed = float(data["speed"])
            except ValueError:
                return json.dumps(
                    {"error": "Invalid speed value"}
                ), 400
        if data.get("fg") is not None:
            try:
                fg = list(map(int, data["fg"]))
            except ValueError:
                return json.dumps(
                    {"error": "Invalid fg value"}
                ), 400
            if len(fg) != 3 or not _isValidColor(fg):
                return json.dumps(
                    {"error": "Invalid color for fg"}
                ), 400
        if data.get("bg") is not None:
            try:
                bg = list(map(int, data["bg"]))
            except ValueError:
                return json.dumps(
                    {"error": "Invalid bg value"}
                ), 400
            if len(bg) != 3 or not _isValidColor(bg):
                return json.dumps(
                    {"error": "Invalid color for bg"}
                ), 400
        # We now have a message to send
        # 1. 'msg' is the only key
        if speed is None and len(data) == 1:
            # Scroll message with default speed
            leds.post_message(msg)
        else:
            # 2. 'msg', 'speed', 'fg', and 'bg' keys
            if speed is not None and fg is not None and bg is not None:
                # Scroll message with speed, fg and bg colors
                leds.post_message(msg, speed, fg, bg)
            # 3. 'msg' and 'speed' keys
            elif speed is not None:
                # Scroll message with speed, white on black colors
                leds.post_message(msg, speed)
            else:
                return json.dumps(
                    {"error": "Invalid message data"}
                ), 400
        return json.dumps({"message": "Message processed"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="::", port=8080)  # nosec

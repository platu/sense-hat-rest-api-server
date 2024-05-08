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
        try:
            for c in color:
                if (c < 0) or (c > 255):
                    return "Invalid color value"
            return "Valid Color"
        except TypeError:
            return "Invalid color type"

    # ----------------------------------------------------------------------------
    # Route for the messages
    @app.route("/api/v1/messages/", methods=["post"], strict_slashes=False)
    def route_messages():
        if _isValidJSON(request.data) is False:
            return json.dumps({"error": "Invalid JSON"}), 400
        else:
            data = request.get_json()
        if "msg" not in data:
            return json.dumps({"error": "Missing 'msg' key"}), 400
        else:
            msg = data["msg"]
            if "speed" in data:
                try:
                    speed = float(data["speed"])
                except ValueError:
                    return json.dumps({"error": "Invalid speed value"}), 400
            else:
                # Back to default speed
                speed = 0.1
            if "fg" in data and "bg" in data:
                if (not _isValidJSON(data["fg"])) or \
                   (not _isValidJSON(data["bg"])):
                    return json.dumps({"error": "Invalid JSON for fg or bg"}), 400
                fg = json.loads(data["fg"])
                bg = json.loads(data["bg"])
                # Test color validity
                # Check if fg and bg are lists with 3 elements
                if isinstance(fg, list) and len(fg) == 3:
                    # Check if each element is between 0 and 255
                    fg_valid = _isValidColor(fg)
                else:
                    fg_valid = "Invalid color type"
                if isinstance(bg, list) and len(bg) == 3:
                    # Check if each element is between 0 and 255
                    bg_valid = _isValidColor(bg)
                else:
                    bg_valid = "Invalid color type"
                if not fg_valid == "Valid Color":
                    return json.dumps({"error": fg_valid}), 400
                if not bg_valid == "Valid Color":
                    return json.dumps({"error": bg_valid}), 400
                # Scroll message with speed, foreground and background colors
                leds.post_message(msg, speed, fg, bg)
            else:
                # Scroll message with or without speed
                leds.post_message(msg, speed)
        return json.dumps({"message": "Message processed"})
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="::", port=8080)  # nosec

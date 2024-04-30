#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/api/v1", code=302)


@app.route("/api/v1", methods=["GET"])
def main():
    main_data = ["sensors", "leds", "messages"]
    return json.dumps(main_data, indent=2)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # nosec

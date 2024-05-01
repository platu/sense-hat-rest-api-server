#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time

from sense_hat import SenseHat

SLEEP_TIME = 200  # in ms
T_SAMPLES = 10


sense = SenseHat()


def _read_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()  # nosec
    t = float(res.replace("temp=", "").replace("'C\n", ""))
    return t


def _read_sense_temp():
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    return (t1 + t2) / 2


def _read_sense_humidity():
    return sense.get_humidity()


def _read_sense_pressure():
    return sense.get_pressure()


# Use moving average of 10 measures to compensate CPU heating
def _avg_temp(t):
    if not hasattr(_avg_temp, "lst"):
        _avg_temp.lst = [t] * 10
    else:
        _avg_temp.lst = _avg_temp.lst[1:]
        _avg_temp.lst.insert(9, t)
    return sum(_avg_temp.lst) / 10


def _estimate_temp():
    for _ in range(T_SAMPLES):
        t_cpu = _read_cpu_temp()
        t_sense = _read_sense_temp()
        t_est = _avg_temp(t_sense - ((t_cpu - t_sense) / 1.5))
        time.sleep(SLEEP_TIME / 1000)
    return t_est


def get_sensors_data():
    """Collects temperature, humidity and pressure measures from the Sense HAT.

    Returns:
        JSON dictionary: temperature, humidity and pressure measures
    """
    sensors_data = {"temperature": "", "humidity": "", "pressure": ""}

    sensors_data["temperature"] = _estimate_temp()
    sensors_data["humidity"] = _read_sense_humidity()
    sensors_data["pressure"] = _read_sense_pressure()

    return json.dumps(sensors_data, indent=2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sense_hat import SenseHat
import json
import os
import time

from multipledispatch import dispatch

SLEEP_TIME = 200  # in ms
T_SAMPLES = 10

sensors_data = {
    "temperature": [],
    "humidity": [],
    "pressure": []
}

sense = SenseHat()


def read_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=", "").replace("'C\n", ""))
    return t


def read_sense_temp():
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    return (t1 + t2) / 2


def read_sense_humidity():
    return sense.get_humidity()


def read_sense_pressure():
    return sense.get_pressure()


# Use moving average of 10 measures to compensate CPU heating
def avg_temp(t):
    if not hasattr(avg_temp, "lst"):
        avg_temp.lst = [t] * 10
    else:
        avg_temp.lst = avg_temp.lst[1:]
        avg_temp.lst.insert(9, t)
        # print(avg_temp.lst)
    return sum(avg_temp.lst) / 10


def estimate_temp():
    for _ in range(T_SAMPLES):
        t_cpu = read_cpu_temp()
        t_sense = read_sense_temp()
        t_est = avg_temp(t_sense - ((t_cpu - t_sense) / 1.5))
        time.sleep(SLEEP_TIME / 1000)
    return t_est


@dispatch()
def get_sensors_data():
    sensors_data["temperature"] = estimate_temp()
    sensors_data["humidity"] = read_sense_humidity()
    sensors_data["pressure"] = read_sense_pressure()
    return json.dumps(sensors_data, indent=2)


@dispatch(str)
def get_sensors_data(sense):  # noqa: F811
    if sense == "temperature":
        return json.dumps({"temperature": estimate_temp()}, indent=2)
    elif sense == "humidity":
        return json.dumps({"humidity": read_sense_humidity()}, indent=2)
    elif sense == "pressure":
        return json.dumps({"pressure": read_sense_pressure()}, indent=2)
    else:
        return json.dumps(sensors_data, indent=2)

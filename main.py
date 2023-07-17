#!/usr/bin/env python
import time
import rainbowhat as rh
from cpu import CPUInfo
from util import Util
from enum import Enum

rh.rainbow.set_clear_on_exit()

class Screen(Enum):
    OFF = 1
    TEMP = 2
    LOAD = 3

currentStat = Screen.TEMP

@rh.touch.A.press()
def touch_a(channel):
    global currentStat
    print("Button A touched!")
    currentStat = Screen.TEMP

@rh.touch.B.press()
def touch_b(channel):
    global currentStat
    print("Button B touched!")
    currentStat = Screen.LOAD

@rh.touch.C.press()
def touch_c(channel):
    global currentStat
    print("Button C touched!")
    currentStat = Screen.OFF


def show_graph(v, r, g, b):
    v *= rh.rainbow.NUM_PIXELS
    for x in range(rh.rainbow.NUM_PIXELS):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
        rh.rainbow.set_pixel(x, r, g, b)
        v -= 1

    rh.rainbow.show()

def display_message(message):
    rh.display.clear()
    rh.display.print_float(message)
    rh.display.show()

rh.rainbow.set_brightness(0.1)

while True:
    temp = round(CPUInfo.get_cpu_temperature() / 100.0, 4)
    load = round(CPUInfo.get_cpu_load() / 100.0, 4)

    print(f"TEMP {temp * 100}, LOAD {load * 100}, MODE {currentStat}")

    if currentStat == Screen.TEMP:
        show_graph(temp, Util.lerp(0, 255, temp), Util.lerp(255, 0, temp), 0)
        display_message(temp * 100)
        rh.lights.rgb(1, 0, 0)
    elif currentStat == Screen.LOAD:
        show_graph(load, Util.lerp(0, 255, load), Util.lerp(255, 0, load), 0)
        display_message(load * 100)
        rh.lights.rgb(0, 1, 0)
    else:
        show_graph(0, 0, 0, 0)
        rh.display.print_str('')
        rh.display.show()
        rh.lights.rgb(0, 0, 1)

    time.sleep(1)
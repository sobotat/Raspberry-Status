#!/usr/bin/env python
import time
from datetime import datetime
import atexit
import signal
import sys
import rainbowhat as rh
from lib.cpu import CPUInfo
from lib.util import Util
from enum import Enum
from logger import Logger, Level

def kill_handler(signal, frame):
    exit_handler()
    sys.exit(1)

def exit_handler():
    logger.log(Level.Info, 'Application Exiting ...')

    rh.rainbow.clear()
    rh.rainbow.show()
    rh.display.clear()
    rh.display.show()
    rh.lights.rgb(0, 0, 0)

    logger.log(Level.Info, 'Application Exited ...')



class Screen(Enum):
    OFF = 1
    TEMP = 2
    LOAD = 3

#Logger Setup
Logger.logToConsole = False
Logger.logToFile = True
Logger.fileName = 'output.log'
logger = Logger('Main')

signal.signal(signal.SIGTERM, kill_handler)
currentStat = Screen.TEMP
defaultTimeToOff = 10
remainingTime = defaultTimeToOff
nightMode = int(datetime.now().strftime("%H")) > 6 and int(datetime.now().strftime("%H")) <= 20

@rh.touch.A.press()
def touch_a(channel):
    global currentStat, remainingTime, defaultTimeToOff, logger
    currentStat = Screen.TEMP
    remainingTime = defaultTimeToOff
    logger.log(Level.Info, 'Screen changed to Temp')

@rh.touch.B.press()
def touch_b(channel):
    global currentStat, remainingTime, defaultTimeToOff, logger
    currentStat = Screen.LOAD
    remainingTime = defaultTimeToOff
    logger.log(Level.Info, 'Screen changed to CPU Load')

@rh.touch.C.press()
def touch_c(channel):
    global currentStat, remainingTime, defaultTimeToOff, logger
    currentStat = Screen.OFF
    remainingTime = 0
    logger.log(Level.Info, 'Screen turned Off')


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

rh.rainbow.set_brightness(0.5)

logger.log(Level.Info, 'Raspberry-Status started ...')
try:
    while True:
        
        if remainingTime >= 0:
            remainingTime = remainingTime - 1
        if remainingTime == 0:
            currentStat = Screen.OFF

        if currentStat == Screen.TEMP:
            temp = round(CPUInfo.get_cpu_temperature() / 100.0, 4)
            show_graph(temp, Util.lerp(0, 255, temp), Util.lerp(255, 0, temp), 0)
            display_message(temp * 100)
            rh.lights.rgb(1, 0, 0)
        elif currentStat == Screen.LOAD:
            load = round(CPUInfo.get_cpu_load() / 100.0, 4)
            show_graph(load, Util.lerp(0, 255, load), Util.lerp(255, 0, load), 0)
            display_message(load * 100)
            rh.lights.rgb(0, 1, 0)
        else:
            show_graph(0, 0, 0, 0)
            rh.display.clear()
            rh.display.show()
            
            currentHour = int(datetime.now().strftime("%H"))
            if nightMode and currentHour > 6 and currentHour <= 20:
                nightMode = False
                logger.log(Level.Info, 'Switching to DayMode')
            elif not nightMode and not(currentHour > 6 and currentHour <= 20):
                nightMode = True
                logger.log(Level.Info, 'Switching to NightMode')

            if not nightMode:
                rh.lights.rgb(0, 0, 1)
            else:
                rh.lights.rgb(0, 0, 0)

        time.sleep(1)

except Exception as e:
    logger.log(str(e))
    exit_handler()
    sys.exit(2)
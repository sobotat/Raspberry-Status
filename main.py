#!/usr/bin/env python
import time, atexit, signal, sys
import rainbowhat as rh
from lib.logger import Logger, Level
from lib.rainbowHatUtil import RainbowHatUtil
from screens.screen import Screen
from screens.tempScreen import TempScreen
from screens.cpuLoadScreen import CPULoadScreen
from screens.offScreen import OffScreen


def kill_handler(signal, frame):
    exit_handler()
    sys.exit(1)

@atexit.register
def exit_handler():
    logger.log(Level.Info, 'Raspberry-Status exiting ...')
    RainbowHatUtil.clear()
    logger.log(Level.Info, 'Raspberry-Status exited ...')

#---------------------------------------------------------------------------------------------

#Logger Setup
Logger.logConsoleToLevel = Level.Off
Logger.logFileToLevel = Level.Info
Logger.fileName = 'output.log'
logger = Logger('Main')

#Kill signal
signal.signal(signal.SIGTERM, kill_handler)

#Screens
tempScreen = TempScreen()
cpuLoadScreen = CPULoadScreen()
offScreen = OffScreen()

currentScreen:Screen = tempScreen

#Default Time to turn off
defaultTimeToOff = 10
remainingTime = defaultTimeToOff

#---------------------------------------------------------------------------------------------

def changeScreen(newScreen:Screen):
    global currentScreen
    currentScreen.deactivated()
    currentScreen = newScreen
    currentScreen.activated()

@rh.touch.A.press()
def touch_a(channel):
    global tempScreen, remainingTime, defaultTimeToOff
    changeScreen(tempScreen)
    remainingTime = defaultTimeToOff

@rh.touch.B.press()
def touch_b(channel):
    global cpuLoadScreen, remainingTime, defaultTimeToOff, logger
    changeScreen(cpuLoadScreen)
    remainingTime = defaultTimeToOff

@rh.touch.C.press()
def touch_c(channel):
    global offScreen, remainingTime, defaultTimeToOff, logger
    changeScreen(offScreen)
    remainingTime = 0

#---------------------------------------------------------------------------------------------

logger.log(Level.Info, 'Raspberry-Status started ...')
try:
    while True:
        
        if remainingTime >= 0:
            remainingTime = remainingTime - 1
        if remainingTime == 0:
            changeScreen(offScreen)

        currentScreen.update()

        time.sleep(1)

except Exception as e:
    logger.log(str(e))
    exit_handler()
    sys.exit(2)
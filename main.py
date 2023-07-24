#!/usr/bin/env python
import time, atexit, signal, sys
import rainbowhat as rh
from lib.logger import Logger, Level
from lib.rainbowHatUtil import RainbowHatUtil
from screens.screen import Screen
from screens.tempScreen import TempScreen
from screens.cpuLoadScreen import CPULoadScreen
from screens.offScreen import OffScreen
from screens.netScreen import NetScreen


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
netScreen = NetScreen()
offScreen = OffScreen()

currentScreen:Screen = tempScreen

#Default Time to turn off
sleepTime = 0.5
defaultTimeToOff = 10 / sleepTime
remainingTime = defaultTimeToOff

#---------------------------------------------------------------------------------------------

def changeScreen(newScreen:Screen):
    global currentScreen
    currentScreen.deactivated()
    currentScreen = newScreen
    currentScreen.activated()

def resetTimeToOff():
    global remainingTime, defaultTimeToOff
    remainingTime = defaultTimeToOff

@rh.touch.A.press()
def touch_a(channel):
    global tempScreen
    changeScreen(tempScreen)
    resetTimeToOff()

@rh.touch.B.press()
def touch_b(channel):
    global cpuLoadScreen
    changeScreen(cpuLoadScreen)
    resetTimeToOff()

@rh.touch.C.press()
def touch_c(channel):
    global netScreen
    changeScreen(netScreen)
    resetTimeToOff()

#---------------------------------------------------------------------------------------------

logger.log(Level.Info, 'Raspberry-Status started ...')
try:
    while True:
        
        if remainingTime >= 0:
            remainingTime = remainingTime - 1
        if remainingTime == 0:
            changeScreen(offScreen)

        currentScreen.update(sleepTime)

        time.sleep(sleepTime)

except Exception as e:
    logger.log(Level.Error, str(e.with_traceback()))
    sys.exit(2)
#!/usr/bin/env python
import time, atexit, signal, sys
from lib.logger import Logger, Level
from lib.rainbowHatUtil import RainbowHatUtil
from screens.screen import Screen
from screens.tempScreen import TempScreen
from screens.cpuLoadScreen import CPULoadScreen
from screens.offScreen import OffScreen
from screens.netScreen import NetScreen

try:
    import rainbowhat as rh
except ImportError:
    print("This script requires the rainbowhat module\nInstall with: sudo pip install rainbowhat")

def kill_handler(signal, frame):
    exit_handler()
    sys.exit(1)

@atexit.register
def exit_handler():
    logger.log(Level.Info, 'Raspberry-Status exiting ...')
    RainbowHatUtil.clear()
    logger.log(Level.Info, 'Raspberry-Status exited')

#---------------------------------------------------------------------------------------------

#Logger Setup
Logger.logConsoleToLevel = Level.Off
Logger.logFileToLevel = Level.All
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

def resetTimeToOff(multiplier=1):
    global remainingTime, defaultTimeToOff
    remainingTime = defaultTimeToOff * multiplier

try:
    @rh.touch.A.press()
    def touch_a(channel):
        global tempScreen, netScreen, currentScreen
        if currentScreen == netScreen:
            logger.log(Level.Warn, 'NetScreen mode changed [Upload]')
            netScreen.showUpload = True
            changeScreen(netScreen)
            resetTimeToOff(multiplier=4)
        else:
            changeScreen(tempScreen)
            resetTimeToOff()

    @rh.touch.B.press()
    def touch_b(channel):
        global cpuLoadScreen, netScreen, currentScreen
        if currentScreen == netScreen:
            logger.log(Level.Warn, 'NetScreen mode changed [Download]')
            netScreen.showUpload = False
            changeScreen(netScreen)
            resetTimeToOff(multiplier=4)
        else:
            changeScreen(cpuLoadScreen)
            resetTimeToOff()

    @rh.touch.C.press()
    def touch_c(channel):
        global netScreen, offScreen, remainingTime
        if currentScreen == netScreen:
            changeScreen(offScreen)
            remainingTime = -1
        else :
            netScreen.showUpload = True
            changeScreen(netScreen)
            resetTimeToOff(multiplier=4)
except NameError:
    print('Failed Create Press Listeners')

#---------------------------------------------------------------------------------------------

logger.log(Level.Info, 'Raspberry-Status started')
try:
    while True:
        
        if remainingTime >= 0:
            remainingTime = remainingTime - 1
        if remainingTime == 0:
            changeScreen(offScreen)

        currentScreen.update(sleepTime)

        time.sleep(sleepTime)

except Exception as e:
    logger.log(Level.Error, str(e))
    sys.exit(2)
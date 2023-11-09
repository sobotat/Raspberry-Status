#!/usr/bin/env python
import time, atexit, signal, sys
from lib.logger import Logger, Level
from lib.avg_monitor import AVG_Monitor

def kill_handler(signal, frame):
    exit_handler()
    sys.exit(1)

@atexit.register
def exit_handler():
    logger.log(Level.Info, 'Raspberry-Monitor exited')

#---------------------------------------------------------------------------------------------

#Logger Setup
Logger.logConsoleToLevel = Level.Off
Logger.logFileToLevel = Level.All
Logger.fileName = 'output_monitor.log'
logger = Logger('Main')

#Kill signal
signal.signal(signal.SIGTERM, kill_handler)

#Default Time to turn off
sleepTime = 0.5
defaultTimeToOff = 10 / sleepTime
remainingTime = defaultTimeToOff

#---------------------------------------------------------------------------------------------

timerWrite = 0
avg_monitor = AVG_Monitor()

logger.log(Level.Info, 'Raspberry-Monitor started')
try:
    while True:

        timerWrite += sleepTime
        if (timerWrite > 15):
            avg_monitor.writeAVGData(timerWrite)
            timerWrite = 0

        time.sleep(sleepTime)

except Exception as e:
    logger.log(Level.Error, str(e))
    sys.exit(2)
from enum import Enum
from datetime import datetime
import threading
import os, sys

class Level(Enum):
    Off = 0
    Error = 1
    Warn = 2
    Info = 3
    Debug = 4
    Trace = 5
    All = 6

    def __str__(self) -> str:
        return super().name

class Logger:

    logConsoleToLevel = Level.Info
    logFileToLevel = Level.Off
    fileName='output.log'
    maxFileSizeInMB = 15

    def __init__(self, className:str) -> None:        
        self.className = className

    def log(self, level:Level, message:str):
        message = self.__getLogText(level, message, datetime.now(), threading.currentThread().getName())
        
        if level.value <= self.logConsoleToLevel.value:
            print(message)
        if level.value <= self.logFileToLevel.value:
            self.__logToFile(message)

    def __getLogText(self, level:Level, message:str, date:datetime, threadName:str) -> str:
        return str(date) + f' [{level}] ' + f'[{threading.currentThread().getName()}] ' + f'[{self.className}] > ' + message

    def __logToFile(self, message:str):
        
        try:
            appPath = Logger.__getPathToRoot()
            fileSize = os.stat(appPath + '\\' + self.fileName).st_size / (1024 * 1024)
            if fileSize >= self.maxFileSizeInMB:
                self.__clearLogFile()
        except FileNotFoundError:
            pass
        except Exception as e:
            print('Clearing File Error: ', str(e))

        file = open(self.fileName, 'at')
        file.write(message + '\n')
        file.close()
        
    def __clearLogFile(self):
        file = open(self.fileName, 'rt')
        lines = file.readlines()
        file.close()

        lenght = int(len(lines)/2)
        print(lenght)       
        lines = lines[lenght:]            

        file = open(self.fileName, 'wt')
        
        for line in lines:
            file.write(line)
        file.close()

    def __getPathToRoot() -> str:
        return os.path.dirname(sys.modules['__main__'].__file__)
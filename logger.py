from enum import Enum
from datetime import datetime
import threading
import os

class Level(Enum):
    Error = 0,
    Warn = 1,
    Info = 2

    def __str__(self) -> str:
        return super().__str__().split('.')[1]

class Logger:

    logToConsole=True, 
    logToFile=False, 
    fileName='output.log'
    maxFileSizeInMB = 15

    def __init__(self, className:str) -> None:        
        self.className = className

    def log(self, level:Level, message:str):
        message = self.__getLogText(level, message, datetime.now(), threading.currentThread().getName())

        if self.logToConsole:
            print(message)
        if self.logToFile:
            self.__logToFile(message)

    def __getLogText(self, level:Level, message:str, date:datetime, threadName:str) -> str:
        return str(date) + f' [{level}] ' + f'[{threading.currentThread().getName()}] ' + f'[{self.className}] > ' + message

    def __logToFile(self, message:str):
        
        try:
            appPath = f"{os.path.dirname(os.path.abspath(__file__))}"
            fileSize = os.stat(appPath + '\\' + self.fileName).st_size / (1024 * 1024)
            if fileSize >= self.maxFileSizeInMB:
                self.__clearLogFile()
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

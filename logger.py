from enum import Enum
from datetime import datetime
import threading

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

    def __init__(self, className:str) -> None:        
        self.className = className

    def log(self, level:Level, message:str):
        message = str(datetime.now()) + f' [{level}] ' + f'[{threading.currentThread().getName()}] ' + f'[{self.className}] > ' + message

        if self.logToConsole:
            print(message)
        if self.logToFile:
            self.__logToFile(message)

    def __logToFile(self, message:str):
        file = open(self.fileName, 'at')
        file.write(message + '\n')
        file.close()
        

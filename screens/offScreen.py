from screens.screen import Screen
from lib.rainbowHatUtil import RainbowHatUtil
from lib.logger import Logger, Level
from datetime import datetime
from lib.avg_writer import AVG_Writer

class OffScreen(Screen):
    
    def __init__(self, dayStartAt:int = 6, dayEndAt:int = 20) -> None:
        super().__init__()
        self.logger = Logger('OffScreen')
        self.dayStartAt = dayStartAt
        self.dayEndAt = dayEndAt

        self.nightMode = self.isDay()
        self.timerWrite = 0
        self.timerPrint = 0
        self.avg_writer = AVG_Writer()

    def update(self, deltaTime):
        if self.nightMode and self.isDay():
            self.nightMode = False
            self.logger.log(Level.Info, 'Switching to DayMode')
            self.avg_writer.avg_monitor.printAvg(clearData=False)
        elif not self.nightMode and not(self.isDay()):
            self.nightMode = True
            self.logger.log(Level.Info, 'Switching to NightMode')
            self.avg_writer.avg_monitor.printAvg(clearData=True)

        if not self.nightMode:
            RainbowHatUtil.show_rgb(0, 0, 1)
        else:
            RainbowHatUtil.show_rgb(0, 0, 0)

        self.timerWrite += deltaTime
        if (self.timerWrite > 10):
            self.avg_writer.writeAVGData(deltaTime)
            self.timerWrite = 0

        self.timerPrint += deltaTime
        if (self.timerPrint > 3600):
            self.avg_writer.avg_monitor.printAvg(clearData=False)
            self.timerPrint = 0

    def activated(self):
        self.logger.log(Level.Warn, 'Off Screen Activated')
        RainbowHatUtil.clear()
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'Off Screen Deactivated')

    def isDay(self):
        currentHour = int(datetime.now().strftime("%H"))
        return currentHour > self.dayStartAt and currentHour < self.dayEndAt
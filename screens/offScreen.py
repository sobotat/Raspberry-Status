from screens.screen import Screen
from lib.rainbowHatUtil import RainbowHatUtil
from lib.logger import Logger, Level
from datetime import datetime

class OffScreen(Screen):
    
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger('OffScreen')

    def update(self):
        currentHour = int(datetime.now().strftime("%H"))
        if nightMode and currentHour > 6 and currentHour <= 20:
            nightMode = False
            self.logger.log(Level.Warn, 'Switching to DayMode')
        elif not nightMode and not(currentHour > 6 and currentHour <= 20):
            nightMode = True
            self.logger.log(Level.Warn, 'Switching to NightMode')        

        if not nightMode:
            RainbowHatUtil.show_rgb(0, 0, 1)
        else:
            RainbowHatUtil.show_rgb(0, 0, 0)

    def activated(self):
        self.logger.log(Level.Warn, 'Off Screen Activated')
        RainbowHatUtil.clear()
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'Off Screen Deactivated')

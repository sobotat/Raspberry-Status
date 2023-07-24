from screens.screen import Screen
from lib.rainbowHatUtil import RainbowHatUtil
from lib.logger import Logger, Level
from lib.cpu import CPUInfo
from lib.util import Util

class TempScreen(Screen):
    
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger('TempScreen')

    def update(self):
        temp = round(CPUInfo.get_cpu_temperature() / 100.0, 4)

        RainbowHatUtil.show_graph(temp, Util.lerp(0, 255, temp), Util.lerp(255, 0, temp), 0)
        RainbowHatUtil.display_message(temp * 100)
        RainbowHatUtil.show_rgb(1, 0, 0)

    def activated(self):
        self.logger.log(Level.Warn, 'Temp Screen Activated')
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'Temp Screen Deactivated')
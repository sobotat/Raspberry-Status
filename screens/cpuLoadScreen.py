from screens.screen import Screen
from lib.rainbowHatUtil import RainbowHatUtil
from lib.logger import Logger, Level
from lib.cpu import CPUInfo
from lib.util import Util

class CPULoadScreen(Screen):
    
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger('CPULoadScreen')

    def update(self, deltaTime):
        load = round(CPUInfo.get_cpu_load() / 100.0, 4)

        RainbowHatUtil.show_graph(load, Util.lerp(0, 255, load), Util.lerp(255, 0, load), 0)
        RainbowHatUtil.display_message(load * 100)
        RainbowHatUtil.show_rgb(0, 1, 0)

    def activated(self):
        self.logger.log(Level.Warn, 'CPU Load Screen Activated')
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'CPU Load Screen Deactivated')
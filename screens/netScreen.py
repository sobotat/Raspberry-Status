from screens.screen import Screen
from lib.rainbowHatUtil import RainbowHatUtil
from lib.logger import Logger, Level
from lib.net import NetInfo, NetUnit
from lib.util import Util

class NetScreen(Screen):
    
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger('NetScreen')
        self.lastUploadBytes = 0
        self.lastDownloadBytes = 0

    def update(self, deltaTime):
        uploadSpeed = NetInfo.getUploadSpeed(deltaTime, self.lastUploadBytes, NetUnit.MB)
        downloadSpeed = NetInfo.getDownloadSpeed(deltaTime, self.lastDownloadBytes, NetUnit.MB)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
        uploadSpeed = uploadSpeed[0]
        downloadSpeed = downloadSpeed[0]

        self.logger.log(Level.Trace, f"Us[{uploadSpeed} MB/s], Ds[{downloadSpeed} MB/s]")

        uploadSpeed = Util.getPercent(0, 50, uploadSpeed)
        RainbowHatUtil.show_graph(uploadSpeed, Util.lerp(0, 255, uploadSpeed), Util.lerp(255, 0, uploadSpeed), 0)
        RainbowHatUtil.display_message(uploadSpeed * 100)
        RainbowHatUtil.show_rgb(1, 1, 0)

    def activated(self):
        self.logger.log(Level.Warn, 'Net Screen Activated')
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'Net Screen Deactivated')
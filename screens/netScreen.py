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
        self.showUpload = True

    def update(self, deltaTime):
        uploadSpeed = NetInfo.getUploadSpeed(deltaTime, self.lastUploadBytes, NetUnit.MB)
        downloadSpeed = NetInfo.getDownloadSpeed(deltaTime, self.lastDownloadBytes, NetUnit.MB)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
        uploadSpeed = round(uploadSpeed[0], 4)
        downloadSpeed = round(downloadSpeed[0], 4)

        self.logger.log(Level.Trace, f"Us[{uploadSpeed} MB/s], Ds[{downloadSpeed} MB/s]")

        if self.showUpload:
            uploadSpeed = round(Util.getPercent(0, 50, uploadSpeed), 4)
            RainbowHatUtil.show_graph(uploadSpeed, Util.lerp(0, 255, uploadSpeed), Util.lerp(255, 0, uploadSpeed), 0)
            RainbowHatUtil.display_message(uploadSpeed * 100)
            RainbowHatUtil.show_rgb(1, 0, 1)
        else:
            downloadSpeed = round(Util.getPercent(0, 50, downloadSpeed), 4)
            RainbowHatUtil.show_graph(downloadSpeed, Util.lerp(0, 255, downloadSpeed), Util.lerp(255, 0, downloadSpeed), 0)
            RainbowHatUtil.display_message(downloadSpeed * 100)
            RainbowHatUtil.show_rgb(0, 1, 1)

    def activated(self):
        self.logger.log(Level.Warn, 'Net Screen Activated')
        uploadSpeed = NetInfo.getUploadSpeed(0.1, self.lastUploadBytes, NetUnit.MB)
        downloadSpeed = NetInfo.getDownloadSpeed(0.1, self.lastDownloadBytes, NetUnit.MB)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'Net Screen Deactivated')
from screens.screen import Screen
from lib.rainbowHatUtil import RainbowHatUtil
from lib.logger import Logger, Level
from lib.net import NetInfo
from lib.util import Util

class NetScreen(Screen):
    
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger('NetScreen')
        self.lastUploadBytes = 0
        self.lastDownloadBytes = 0

    def update(self, deltaTime):
        uploadSpeed = NetInfo.getUploadSpeed(deltaTime, self.lastUploadBytes)
        downloadSpeed = NetInfo.getDownloadSpeed(deltaTime, self.lastDownloadBytes)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
        uploadSpeed = uploadSpeed[0]
        downloadSpeed = downloadSpeed[0]
        
        upload = NetInfo.getUpload()
        download = NetInfo.getDownload

        self.logger.log(Level.Trace, f"U[{upload[0]} {upload[1]}], D[{download[0]} {download[1]}], Us[{uploadSpeed}/s], Ds[{downloadSpeed}/s]")

        RainbowHatUtil.show_graph(uploadSpeed, Util.lerp(0, 255, uploadSpeed), Util.lerp(255, 0, uploadSpeed), 0)
        RainbowHatUtil.display_message(uploadSpeed * 100)
        RainbowHatUtil.show_rgb(1, 0, 0)

    def activated(self):
        self.logger.log(Level.Warn, 'Net Screen Activated')
    
    def deactivated(self):
        self.logger.log(Level.Warn, 'Net Screen Deactivated')

from lib.avg_monitor import AVG_Monitor
from lib.cpu import CPUInfo
from lib.net import NetInfo, NetUnit
from lib.database import Database
from random import Random
from datetime import datetime

class AVG_Writer:
    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AVG_Writer, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if AVG_Writer.__instance is None:
            AVG_Writer.__instance = self
            self.lastUploadBytes = NetInfo.getUploadSpeed(0.1, 0, NetUnit.KB)[1]
            self.lastDownloadBytes = NetInfo.getDownloadSpeed(0.1, 0, NetUnit.KB)[1]
            self.avg_monitor = AVG_Monitor()

    def writeAVGData(self, deltaTime, sendData:bool = True):
        if (deltaTime == 0):
            deltaTime = 0.1
            
        uploadSpeed = NetInfo.getUploadSpeed(deltaTime, self.lastUploadBytes, NetUnit.KB)
        downloadSpeed = NetInfo.getDownloadSpeed(deltaTime, self.lastDownloadBytes, NetUnit.KB)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
        uploadSpeed = round(uploadSpeed[0], 4)
        downloadSpeed = round(downloadSpeed[0], 4)

        cpu = CPUInfo.get_cpu_load()
        temp = CPUInfo.get_cpu_temperature()

        self.avg_monitor.addData(
            cpu=cpu,
            temp=temp,
            upload=uploadSpeed,
            download=downloadSpeed,
        )

        if (sendData):
            self.sendAVGData(cpu, temp, uploadSpeed, downloadSpeed)

    def sendAVGData(self, cpu, temp, upload, download):
        insert_query = "INSERT INTO raspberry_data (time, cpu, temp, upload, download) VALUES (%s, %s, %s, %s, %s)"

        database = Database()
        database.send(insert_query, (datetime.now(), cpu, temp, upload, download))
from lib.cpu import CPUInfo
from lib.net import NetInfo, NetUnit
from lib.database import Database
from lib.docker import Docker
from random import Random
from datetime import datetime

class AVG_Monitor:
    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AVG_Monitor, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if AVG_Monitor.__instance is None:
            AVG_Monitor.__instance = self
            self.lastUploadBytes = NetInfo.getUploadSpeed(0.1, 0, NetUnit.KB)[1]
            self.lastDownloadBytes = NetInfo.getDownloadSpeed(0.1, 0, NetUnit.KB)[1]
            self.docker = Docker()

    def writeAVGData(self, deltaTime):
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

        self.sendAVGData(cpu, temp, uploadSpeed, downloadSpeed)
        self.docker.sendContainersData()

    def sendAVGData(self, cpu, temp, upload, download):
        insert_query = "INSERT INTO raspberry_data (time, cpu, temp, upload, download) VALUES (%s, %s, %s, %s, %s)"

        database = Database()
        database.send(insert_query, (datetime.now(), cpu, temp, upload, download))
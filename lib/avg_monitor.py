from lib.info import CPUInfo, MemoryInfo
from lib.net import NetInfo, NetUnit
from lib.database import Database
from lib.docker_api import DockerApi
from lib.ssh_api import SSHApi
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
            self.dockerApi = DockerApi()

    def writeAVGData(self, deltaTime):
        if (deltaTime <= 0):
            deltaTime = 0.1
            
        uploadSpeed = NetInfo.getUploadSpeed(deltaTime, self.lastUploadBytes, NetUnit.KB)
        downloadSpeed = NetInfo.getDownloadSpeed(deltaTime, self.lastDownloadBytes, NetUnit.KB)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
        uploadSpeed = round(uploadSpeed[0], 4)
        downloadSpeed = round(downloadSpeed[0], 4)

        cpu = CPUInfo.get_cpu_load()
        memory = MemoryInfo.get_memory_usage()["percent"]
        temp = CPUInfo.get_cpu_temperature()

        sshApi = SSHApi()
        users = sshApi.getUsers()
        active_ssh = len(sshApi.getActiveUsers(users))

        self.sendAVGData(cpu, temp, uploadSpeed, downloadSpeed, memory, active_ssh)
        self.dockerApi.sendContainersData()

    def sendAVGData(self, cpu, temp, upload, download, memory, active_ssh):
        insert_query = "INSERT INTO raspberry_data (time, cpu, temp, upload, download, memory, active_ssh) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        database = Database()
        database.send(insert_query, (datetime.utcnow(), cpu, temp, upload, download, memory, active_ssh))

class AVG_Monitor:

    def __init__(self) -> None:
        self.cpuData = []
        self.tempData = []
        self.uploadData = []
        self.downloadData = []

        self.lastAvgCpu = 0
        self.lastAvgTemp = 0
        self.lastAvgUpload = 0
        self.lastAvgDownload = 0

    def addData(self, cpu:float, temp:float, upload:int, download:int):
        self.cpuData.append(cpu)
        self.tempData.append(temp)
        self.uploadData.append(upload)
        self.downloadData.append(download)

    def computeAvg(self, clearData:bool = True):
        try:
            self.lastAvgCpu = round(sum(self.cpuData) / len(self.cpuData) * 1000) / 1000
            self.lastAvgTemp = round(sum(self.tempData) / len(self.tempData) * 1000) / 1000
            self.lastAvgUpload = round(sum(self.uploadData) / len(self.uploadData) * 1000) / 1000
            self.lastAvgDownload = round(sum(self.downloadData) / len(self.downloadData) * 1000) / 1000

            if clearData: 
                self.clear()
        except:
            return (0, 0, 0, 0)
        return (self.lastAvgCpu, self.lastAvgTemp, self.lastAvgUpload, self.lastAvgDownload)
        
    def clear(self):
        self.cpuData.clear()
        self.tempData.clear()
        self.uploadData.clear()
        self.downloadData.clear()

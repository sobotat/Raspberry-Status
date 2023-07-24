from enum import Enum
try:
    import psutil
except ImportError:
    exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

class NetUnit(Enum):
    B = 0
    KB = 1000
    MB = 1000000
    GB = 1000000000

class NetInfo:

    def getSpeedAndUnit(bytes) -> tuple[int, str]:
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return (bytes, f"{unit}B")
            bytes /= 1024

    def getUpload() -> tuple[int, str]:
        return NetInfo.getSpeedAndUnit(psutil.net_io_counters().bytes_sent)

    def getDownload() -> tuple[int, str]:
        return NetInfo.getSpeedAndUnit(psutil.net_io_counters().bytes_recv)
    
    def getUploadSpeed(updateTime, lastBytesSent, unit:NetUnit) -> tuple[int, int]:
        io = psutil.net_io_counters()
        uploadSpeed = io.bytes_sent - lastBytesSent
        return (uploadSpeed / updateTime / unit.value, io.bytes_sent)

    def getDownloadSpeed(updateTime, lastBytesRecv, unit:NetUnit) -> tuple[int, int]:
        io = psutil.net_io_counters()
        downloadSpeed = io.bytes_recv - lastBytesRecv
        return (downloadSpeed / updateTime / unit.value, io.bytes_recv)
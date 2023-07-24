try:
    import psutil
except ImportError:
    exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

class NetInfo:

    def getSpeedAndUnit(bytes) -> tuple[int, str]:
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return (bytes:.2f, f"{unit}B")
            bytes /= 1024

    def getUpload() -> tuple[int, str]:
        return NetInfo.getSpeedAndUnit(psutil.net_io_counters().bytes_sent)

    def getDownload() -> tuple[int, str]:
        return NetInfo.getSpeedAndUnit(psutil.net_io_counters().bytes_recv)
    
    def getUploadSpeed(updateTime, lastBytesSent) -> tuple[int, int]:
        io = psutil.net_io_counters()
        uploadSpeed = io.bytes_sent - lastBytesSent
        return (uploadSpeed / updateTime, io.bytes_sent)

    def getDownloadSpeed(updateTime, lastBytesRecv) -> tuple[int, int]:
        io = psutil.net_io_counters()
        downloadSpeed = io.bytes_recv - lastBytesRecv
        return (downloadSpeed / updateTime, io.bytes_recv)
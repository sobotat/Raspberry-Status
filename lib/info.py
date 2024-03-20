from subprocess import PIPE, Popen
try:
    import psutil
except ImportError:
    exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

class CPUInfo:
    def get_cpu_temperature():
        temp = -1
        try:
            process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
            output, _error = process.communicate()
            output = output.decode()

            pos_start = output.index('=') + 1
            pos_end = output.rindex("'")

            temp = float(output[pos_start:pos_end])
        except:
            pass
        return temp

    def get_cpu_load():
        return psutil.cpu_percent()
    
class MemoryInfo:
    def get_memory_usage():
        memory = psutil.virtual_memory()
        
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "free": memory.free,
            "percent": memory.percent
        }
    
class DiskInfo:
    def get_disk_usage():
        partitions = psutil.disk_partitions()
        disk_usage = {}
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
            except PermissionError:
                # This happens if a disk is not ready to be read
                pass
        return disk_usage
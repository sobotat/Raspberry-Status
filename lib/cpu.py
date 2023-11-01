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
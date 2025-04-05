import datetime
import sys
from os import listdir, mkdir, path, getpid
import psutil
import wmi


class LogLevel:
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    STARTUP = "STARTUP"


class CreateLogger:
    """
    Redirect stdout and stderr into the Log object
    """
    def __init__(self, log_path='./logs'):
        """
        Redirects stdout and stderr into the Log object, pass in a path to change save location
        :param log_path: path-like: Path to save log files
        """
        sys.stdout = Log(log_path=log_path)
        sys.stderr = sys.stdout


class Log(object):
    """
    The object that redirects stdout
    """
    def __init__(self, log_path='./logs'):
        if not path.isdir(log_path):
            mkdir(log_path)
        self.log_num = len(listdir(log_path))
        self.orgstdout = sys.stdout
        self.log_name = f"{log_path}/log_" + str(self.log_num) + ".txt"

    def write(self, msg):
        self.log = open(self.log_name, "a")
        if self.orgstdout:
            self.orgstdout.write(msg)
        self.log.write(msg)
        self.log.close()

    def flush(self):
        pass


def log_startup():
    """
    Logs relevant system info for future debugging
    :return: None
    """
    print("STARTUP:", datetime.datetime.now().strftime("%c"))
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]
    print(f"STARTUP: Manufacturer - {my_system.Manufacturer}")
    print(f"STARTUP: Model - {my_system.Model}")
    print(f"STARTUP: Name - {my_system.Name}")
    print(f"STARTUP: NumberOfProcessors - {my_system.NumberOfProcessors}")
    print(f"STARTUP: SystemType - {my_system.SystemType}")
    print(f"STARTUP: SystemFamily - {my_system.SystemFamily}")
    svmem = psutil.virtual_memory()
    print(f"STARTUP: Physical Memory Total - {get_size(svmem.total)}")
    print(f"STARTUP: Physical Memory Available - {get_size(svmem.available)}")
    print(f"STARTUP: Physical Memory Used - {get_size(svmem.used)}")
    print(f"STARTUP: Physical Memory Percentage - {svmem.percent}%")
    swap = psutil.swap_memory()
    print(f"STARTUP: Swap Memory Total - {get_size(swap.total)}")
    print(f"STARTUP: Swap Memory Free - {get_size(swap.free)}")
    print(f"STARTUP: Swap Memory Used - {get_size(swap.used)}")
    print(f"STARTUP: Swap Memory Percentage - {swap.percent}%")


def get_process_memory():
    print(f"INFO: {datetime.datetime.now().strftime('%c')}")
    print(f"INFO: Process Memory - {psutil.Process().memory_info().rss / 1024 ** 2:.2f} MB")
    print(f"INFO: RAM Usage - {psutil.virtual_memory()[2]}%")
    svmem = psutil.virtual_memory()
    print(f"INFO: Physical Memory Used - {get_size(svmem.used)}")
    print(f"INFO: Physical Memory Percentage - {svmem.percent}%")
    swap = psutil.swap_memory()
    print(f"INFO: Swap Memory Used - {get_size(swap.used)}")
    print(f"INFO: Swap Memory Percentage - {swap.percent}%")


def parse_log(log_file):
    """
    Parses a log file into a list of lists containing the messages logged
    :param log_file: path-like: Path to the log file
    :return: list of lists containing messages in the log file
    """
    parsed_logs = [[] for i in range(5)]
    with open(log_file, 'r') as f:
        for line in f.readlines():
            parts = line.split(':')
            for i in range(0, len(parts)):
                parts[i] = parts[i].strip()
            if parts[0] == LogLevel.ERROR:
                parsed_logs[0].append(":".join(parts[1:]))
            elif parts[0] == LogLevel.WARNING:
                parsed_logs[1].append(":".join(parts[1:]))
            elif parts[0] == LogLevel.INFO:
                parsed_logs[2].append(":".join(parts[1:]))
            elif parts[0] == LogLevel.STARTUP:
                parsed_logs[3].append(":".join(parts[1:]))
            else:
                parsed_logs[3].append(line)
    return parsed_logs


def get_size(byte_array, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if byte_array < factor:
            return f"{byte_array:.2f}{unit}{suffix}"
        byte_array /= factor

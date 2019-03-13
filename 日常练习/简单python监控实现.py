import psutil
import time
import socket


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()

def log_generate():
    cpu_percent = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    mem_percent = int(mem.used / mem.total * 100)
    disk_partition = psutil.disk_partitions()
    disk_percent = {mount_point : '{} %'.format(psutil.disk_usage('{}'.format(mount_point))[3]) \
                    for mount_point in ( dp.mountpoint for dp in disk_partition )}

    return {get_ip_address():{'cpu': '{} %'.format(cpu_percent), \
                              'mem': '{} %'.format(mem_percent), \
                              'disk':disk_percent, \
                              'time':int(time.time())}}

def open_file(filepath):
    f = open(filepath,'a')
    return f
def close_file(f):
    f.close()

def main(filepath,counttime=1*60*60,interval=5):
        f = open_file(filepath)
        while counttime > 0:
            ret = str(log_generate())
            print(ret)
            f.write(ret + '\n')
            time.sleep(interval)
            counttime -= interval
        close_file(f)

if __name__ == '__main__':
    filepath = 'D:\\log.txt'
    main(filepath)

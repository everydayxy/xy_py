#!/usr/bin/env python
# coding:utf8
import threading
import time
import paramiko
import argparse
from update_file import get_remote_host
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def argument():
    parse = argparse.ArgumentParser()
    parse.add_argument('--thread-number', '-t',dest='num_value', help='thread number')
    parse.add_argument('--command-line', '-c', dest='cmd_value', help='command line')
    args = parse.parse_args()
    return args

def get_hosts():
    update_list = []
    host_lists = get_remote_host()
    for host_name in host_lists:
        for num in range(int(host_name[1][0]),int(host_name[1][1])+1):
            update_list.append('%s-%03d' % (host_name[0],num))

    return update_list

def get_exists_host():
    list1 = []
    hosts_lists = []
    file_lists = get_hosts()
    with open('/etc/hosts','rt') as f:
        for line in f.readlines():
            if line and '#' not in line and len(line.split()) == 2:
                hosts_lists.append(line.split()[1])
    for x in file_lists:
        if x in hosts_lists:
            list1.append(x)

    return list1

def remote_ssh(ip,cmd):
    semaphore.acquire()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip)
        stdin, stdout, stderr = client.exec_command(cmd)
        print (stdout.read())
        print (stderr.read())
        client.close()
    except:
        print('没连上这个服务器')
    semaphore.release()


def main(cmd,method,thread_num=1):
    obj = []
    update_hosts = get_exists_host()
#    print(update_hosts,cmd,method)
    for ip in update_hosts:
        t = threading.Thread(target=method, args=(ip, cmd))
        obj.append(t)
    global semaphore
    semaphore  = threading.BoundedSemaphore(int(thread_num))
    for t in obj:
        t.start()
    while threading.active_count() != 1:
        pass
    else:
        print('所有服务器执行完毕')

if __name__ == '__main__':
    args = argument()
    main(args.cmd_value,remote_ssh,args.num_value)
#!/usr/bin/env python
# coding:utf8
import threading
import time
import paramiko
import argparse
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class run(object):
    def __init__(self):
        from update_file import get_remote_host
        self.host_lists = get_remote_host()

    def argument(self):
        parse = argparse.ArgumentParser()
        parse.add_argument('--thread-number', '-t', dest='num_value', help='thread number')
        parse.add_argument('--command-line', '-c', dest='cmd_value', help='command line')
        args = parse.parse_args()
        return args

    def get_hosts(self):
        update_list = []
        # host_lists = get_remote_host()
        for host_name in self.host_lists:
            for num in range(int(host_name[1][0]), int(host_name[1][1]) + 1):
                update_list.append('%s-%03d' % (host_name[0], num))

        return update_list

    def get_exists_host(self):
        list1 = []
        hosts_lists = []
        file_lists = self.get_hosts()
        with open('/etc/hosts', 'rt') as f:
            for line in f.readlines():
                if line and  len(line.split()) >= 2:
                    hosts_lists.append(line.split()[1])
        for x in file_lists:
            if x not in hosts_lists:
                continue
	    list1.append(x)

        return list1

    def remote_ssh(self, ip, cmd):
        self.semaphore.acquire()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip)
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read())
            print(stderr.read())
            client.close()
        except:
            print('没连上这个服务器')
        self.semaphore.release()

    def main(self, cmd, method, thread_num=1):
        obj = []
        self.update_hosts = self.get_exists_host()
#        for i in self.update_hosts:
#           print(i)
	try:
	    r = raw_input('本次需要更新以下服务器：{},服务器数量：{}，服务器更新命令：{}，确认按1：'.format(self.host_lists,len(self.update_hosts),cmd))
	    if len(r) ==  1 and r.isdigit() and int(r) == 1:
                pass
	    else:
	        return False
        except:
            print
	    return False
        for ip in self.update_hosts:
            t = threading.Thread(target=method, args=(ip, cmd))
            obj.append(t)

        self.semaphore = threading.BoundedSemaphore(int(thread_num))
        for t in obj:
            t.start()
        while threading.active_count() != 1:
            pass
        else:
            print('所有服务器执行完毕')


if __name__ == '__main__':
    AAA = run()
    args = AAA.argument()
    AAA.main(args.cmd_value, AAA.remote_ssh, args.num_value)
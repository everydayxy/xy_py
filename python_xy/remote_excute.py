#!/usr/bin/env python
# coding:utf8

import logging
import paramiko
import argparse
import sys
from concurrent import futures
import time
from progressbar import *


reload(sys)
sys.setdefaultencoding('utf8')


class run(object):
    def __init__(self):
        from update_file import getPlatform
        self.host_lists = getPlatform()
	    self.normal = open('normal.log','w')
	    self.error = open('error.log','w')
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='game_update.log',
                            filemode='w')

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
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip)
            stdin, stdout, stderr = client.exec_command(cmd)
            new_std_out = stdout.read()
            new_std_err = stderr.read()
            logging.info('{}\n{}'.format(ip,new_std_out))
            logging.error('{}\n{}'.format(ip,new_std_err))
	        #self.normal.write('{}:\n{}\n'.format(ip,new_std_out))
	        #self.normal.flush()
            #self.error.write('{}:\n{}\n'.format(ip,new_std_err))
            #self.error.flush()
            client.close()
        except:
            logging.error('没连上这个服务器')
        return new_std_out,new_std_err


    def main(self, cmd, method, thread_num=1):
        self.update_hosts = self.get_exists_host()
        #for i in self.update_hosts:
         #  print(i)
        try:
            r = raw_input('本次需要更新以下服务器：{},服务器数量：{}，服务器更新命令：{}，确认按1：'.format(self.host_lists,len(self.update_hosts),cmd))
            if len(r) ==  1 and r.isdigit() and int(r) == 1:
                    pass
            else:
                return False
        except:
            print
            return False
        obj_dict = dict()
        total_host = len(self.update_hosts)
        current_hostname = 1

        progress = ProgressBar()
        proceed_progress = progress(range(total_host))

        with futures.ThreadPoolExecutor(max_workers=int(thread_num)) as executor:
            for ip in self.update_hosts:
                e = executor.submit(method,ip,cmd)
                obj_dict[e] = ip
            for future in futures.as_completed(obj_dict):
                host_name = obj_dict[future]
                if future.exception() is not None:
                    logging.error('generated an exception: %s' % (future.exception()))
                else:
                    n,e = future.result()
                    logging.info('percent: {1:0.2f}%,  excuting host: {0} '.format(
                        host_name,(current_hostname/float(total_host))*100)
                    )
                    proceed_progress.__next__()
                    if n:
                        self.normal.write('{}:\n{}'.format(host_name,n))
                        self.normal.flush()
                    if e:
                        self.error.write('{}:\n{}'.format(host_name,e))
                        self.error.flush()
                    current_hostname +=1

        try:
            proceed_progress.__next__()
        except StopIteration:
            print
        self.normal.close()
        self.error.close()

if __name__ == '__main__':
    AAA = run()
    args = AAA.argument()
    AAA.main(args.cmd_value, AAA.remote_ssh, args.num_value)


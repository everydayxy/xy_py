#!/usr/bin/env python
# coding:utf8

import os
import time,random
import paramiko
from py_threading_pool import *
from optparse import OptionParser
BLACK = '\033[0;30m'
DARK_GRAY = '\033[1;30m'
LIGHT_GRAY = '\033[0;37m'
BLUE = '\033[0;34m'
LIGHT_BLUE = '\033[1;34m'
GREEN = '\033[0;32m'
LIGHT_GREEN = '\033[1;32m'
CYAN = '\033[0;36m'
LIGHT_CYAN = '\033[1;36m'
RED = '\033[0;31m'
LIGHT_RED = '\033[1;31m'
PURPLE = '\033[0;35m'
LIGHT_PURPLE = '\033[1;35m'
BROWN = '\033[0;33m'
YELLOW = '\033[1;33m'
WHITE = '\033[1;37m'
DEFAULT_COLOR = '\033[00m'
RED_BOLD = '\033[01;31m'
ENDC = '\033[0m'


class Remote(object):
    def __init__(self):
        self.requests = list()
        self.request_total = 0
        self.count = 0
        self.width = 100;
        self.know_hosts = list();
        self._options = None
        self._args = None
        self.getKnowHosts()
        self._ssh = list();
        self._fail_ssh_client = list()
        self._is_block = True  #是否阻塞
        self._getAllHost()
        self._parseArgs()
        self._thread_num = 40;
        self._cmd = "ls"
        if self._options.is_block is not None:  #是否有传阻塞设置
            self._is_block = self._options.is_block
        if self._options.th_num is not None:
            self._thread_num = int(self._options.th_num)
        if self._args.__len__() != 0:
            self._cmd = self._args[0]
        self._error_fp = open("./errmsg.txt","w");
        self._normal_fp = open("./normal.txt","w");

    def __del__(self):
        if self._fail_ssh_client.__len__() and hasattr(self,'_error_fp'):
            self._error_fp.write("-"*20)
            self._error_fp.write("\n更新失败服务器:{}".format(",".join(self._fail_ssh_client)))
        hasattr(self,'_error_fp') and self._error_fp.close();
        hasattr(self,'_normal_fp') and self._normal_fp.close();

    def _getPlatforms(self):
        from update_servers import getPlatform
        return getPlatform()

    def getSshClient(self,host,*args,**kwds):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=host)
            stdin, stdout, stderr = ssh.exec_command(self._cmd)    
            if self._is_block:
                stdout.channel.recv_exit_status()
        except:
            self._fail_ssh_client.append(host)
            stdin,stdout,stderr = (None,None,None)
        return (stdout,stderr)

    def _process(self,msg): 
        sys.stdout.write(' ' * (self.width + 30) + '\r')
        sys.stdout.flush()
        print msg
        progress = self.width * self.count / self.request_total
        sys.stdout.write('{0}/{1}: '.format(self.count, self.request_total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) )
        sys.stdout.write(' ' * 5 + '[{0:.2f}%]\r'.format(self.count / (self.request_total * 1.0) * 100) )
        
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()
       
    def getResult(self,request,result,*args, **kwds):
        self.count += 1
        msg = "该服务器:{} 操作完成".format(request.args[0])
        self._process(msg)
        stdout,stderr = result
        if stdout is None:
            return False
        if self._is_block is False:
            stdout.channel.recv_exit_status()
        errmsg = stderr.read();
        if errmsg.__len__() > 0:
            self._error_fp.write("{0}:{1}".format(request.args[0],errmsg))
            self._error_fp.flush()
        normal = stdout.read();
        if normal.__len__() > 0: 
            self._normal_fp.write("{0}:{1}".format(request.args[0],normal));
            self._normal_fp.flush()
        if stdout.channel.transport.isAlive():
            stdout.channel.transport.close()

    def _getAllHost(self):
        platforms = self._getPlatforms()
        for pl in platforms:
            name,nums = pl
            for num in range(nums[0],nums[1] + 1):
                host = "%s-%03d" % (name,num) 
                if host not in self.know_hosts: 
                    continue
                self.requests.append(host)
        self.request_total = self.requests.__len__()
                


    def getKnowHosts(self):
        know_hosts = list()
        fp = open("/etc/hosts","r")
        lines = fp.readlines()
        for line in lines:
            line = line.strip().split()[0:2]
            if len(line) >= 2:
                ipaddr,alias = line[0:2]
                know_hosts.append(alias)
        self.know_hosts = know_hosts

    def _parseArgs(self):
        optparse = OptionParser()
        optparse.add_option('-t','--tnum',dest="th_num",help="指定同时更新服务器数量".decode("utf-8"))
        optparse.add_option('-f','--filename',dest="filename",help="要运行的脚本文件".decode("utf-8"))
        optparse.add_option('-b','--block', action="store_false" ,dest="is_block",help="是否停用IO阻塞".decode("utf-8"))

        self._options,self._args =  optparse.parse_args()


    def _tip(self):
        vstr = "本次将更新{0}{1}{2}个服务器,执行命令:{5}{3}{2},其中包括{6}{4}{2}请确认,1:继续,其它退出: "
        try:
            r = raw_input(vstr.format(RED,self.request_total,ENDC,self._cmd,self._getPlatforms(),GREEN,CYAN))
            if len(r) ==  1 and r.isdigit() and int(r) == 1:
                return True
            return False
        except:
            print 
            return False

    def main(self):
        if self._tip() is False:
            return False
        self._process("")
        pool = ThreadPool(self._thread_num,0,0)
        for host in self.requests:
            req = WorkRequest(self.getSshClient,args=[host],kwds={},callback=self.getResult)
            pool.putRequest(req)
        while True:
            try:
                time.sleep(0.5)
                pool.poll()
            except NoResultsPending:
                break
            except NoWorkersAvailable:
                pass
        pool.stop()


if __name__ == '__main__':
    model = Remote()
    model.main()

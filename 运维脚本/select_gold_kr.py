#!/usr/bin/env python
# coding:utf8
'''
查询韩国游戏服务器各种类型的金币消耗
python select_gold_kr.py   '7,9'
'''

import urllib2
import json
import paramiko
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
#pingtai = [['koreaios', '1,2000'], ['korea', '1,2000'], ['koreaand', '1,2000'], ['koreagoogle', '1,2000']]
pingtai = [['koreagoogle', '1,2000']]

# 获取要更新的服务器
def createhostname(tags):
    hosts = gethosts()
    newhost = []
    for tag in tags:
        head, tail = tag[0], tag[1]
        statnum,endnum = tail.split(',')
        for num in range(int(statnum), int(endnum)+1):
            num = '%03d' % num
            host = '{}-{}'.format(head, num)
            if host in hosts:
                newhost.append(host)
            else:
                pass
    return newhost


# 获取 /etc/hosts 里面的所有服务器信息
def gethosts():
    hostlist = []
    data = os.popen("cat /etc/hosts  | awk -F ' '  '{print $2}'")
    for line in data.readlines():
        if line.strip('\n'):
            hostlist.append(line.strip('\n'))
        else:
            pass
    return hostlist


#获取服务器的id
def ssh_client(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host)
        stdin, stdout, stderr = ssh.exec_command('python /mnt/db.bak/xl/qjf/getid.py')
        return stdout.read()
    except:
        return '服务器连接失败！'


#获取数据
def getdate(url, code):
    mydict = {}
    http = urllib2.urlopen(url)
    for line in http.readlines():
        line2 = line.split('|')
        if line2[-3] == code or line2[-3] == str(code):
            if int(line2[-2]) == 0:
                continue
            if mydict.has_key(line2[-2]):
                mydict[line2[-2]] += int(line2[-4])
            else:
                mydict[line2[-2]] = int(line2[-4])
        else:
            pass
    return mydict


def getdatadict():
    datadict = {}
    for i in createhostname(pingtai):
        try:
            hostid = ssh_client(i).strip()
        except:
            continue
        a = sys.argv[1]
#a = '10,12'
        for num in range(int(a.split(',')[0]), int(a.split(',')[1]) + 1):
	    try:
              url = 'http://10.200.27.29/rest/data/GoldFlow?game_id=wly&server_id=%s&start_time=2017-%s-01&end_time=2017-%s-31' % (hostid, str('%s' % num), str('%s' % num))
	      datas = getdate(url, '2')
	    except:
              url = 'http://10.200.27.29/rest/data/GoldFlow?game_id=wly&server_id=%s&start_time=2017-%s-01&end_time=2017-%s-30' % (hostid, str('%s' % num), str('%s' % num))
	      datas = getdate(url, '2')
            for key, val in datas.items():
                if datadict.has_key('{}_{}_{}'.format(i.split('-')[0], key, num)):
                    datadict['{}_{}_{}'.format(i.split('-')[0], key, num)] += val
                else:
                    datadict['{}_{}_{}'.format(i.split('-')[0], key, num)] = val
    return datadict


def main():
#   print('查询开始：%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))o
      for key, val in getdatadict().items():
          print('{},{}'.format(key, val))
#    print('查询结束：%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


if __name__ == '__main__':
    main()







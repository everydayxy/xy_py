#!/usr/bin/env python
# coding:utf8

import paramiko
import sys
import threading
import os

#此脚本需要在同一目录下存放mx_hefu_server_list.txt文件
#mx_hefu_server_list.txt存放需要合服的区服列表,合服所在的区服放在文件第一行
def get_text():
    new_list = []
    with open('mx_hefu_server_list.txt','r') as f:
        for i in f.readlines():
	    new_list.append(i.strip('\n'))
    return new_list

def remote_ssh(ip,cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip)
    stdin, stdout, stderr = client.exec_command(cmd)
    print (stdout.read())
    print (stderr.read())
    client.close()

def remote_exec(method,cmd):
    obj = []
    hefu_server_list = get_text()
    print(hefu_server_list)
    for host in hefu_server_list:
        t = threading.Thread(target=method,args=(host,cmd))
        obj.append(t)
    for t in obj:
        t.setDaemon(True)
        t.start()
    for t in obj:
        t.join()

def tip(hefu_server_list):
        vstr = "{0}即将开始合服准备操作，合服列表为{1}，请确认，1:继续,其它退出{2}"
        try:
            r = raw_input(vstr.format('\033[1;33m',hefu_server_list,'\033[0m'))
            if len(r) ==  1 and r.isdigit() and int(r) == 1:
                return True
            return False
        except:
            print
            return False


def main():
    global hefu_server_list
    hefu_server_list = get_text()
    ret = []
    ret_db = []
    for i in hefu_server_list:
        ret.append('mx-{}.sql'.format(i))
        ret_db.append('mx-{}'.format(i).replace('-','_'))
    hefu_new_list = ','.join(ret)
    game_version = str(raw_input('{}请输入mengxin合服版本(格式为1.3.1): {}'.format('\033[1;33m','\033[0m')))
    print('合服列表在此：{}'.format(hefu_new_list))
    print('合服版本在此：{}'.format(game_version))
    print('删除数据库列表在此：{}'.format(ret_db))
    print('合成数据库将导入：{}'.format(hefu_server_list[0]))
#   print('sudo  php comb_{0}.php -m test -s {1} -v {0} > tmp.log'.format(game_version,hefu_new_list))
    if tip(hefu_server_list) is False:
        return False
    remote_exec(remote_ssh,'sudo /mnt/db.bak/xl/end_game.py')
    remote_ssh(hefu_server_list[0],'sudo pg_dump -h db -U postgres mengxin -sf /mnt/db.bak/data/mengxin/v{}_schema.sql'.format(game_version))
    for k,host in enumerate(hefu_server_list):
        remote_ssh(host,'sudo pg_dump -h db -U postgres mengxin -f /mnt/db.bak/data/mengxin/$(hostname).sql')
        if k != 0:
            remote_ssh(host,'sudo /mnt/db.bak/xl/shell_xl/changeHostname.sh debain')

    print('{}开始合服{}'.format('\033[1;33m','\033[0m'))
    os.system('cd /mnt/data/data/mengxin/ && sudo  php comb_{0}.php -m test -s {1} -v {0} '.format(game_version,hefu_new_list))
    for i in ret_db:
        os.system('dropdb -h db -U postgres {}'.format(i))
    print('{}合服脚本执行完成{}'.format('\033[1;33m','\033[0m'))
    print('{}开始在{}上导入合服数据{}'.format('\033[1;33m',hefu_server_list[0],'\033[0m'))
    remote_ssh(hefu_server_list[0],'dropdb -h db -U postgres mengxin')
    remote_ssh(hefu_server_list[0],'createdb -h db -U postgres mengxin')
    remote_ssh(hefu_server_list[0],'psql -h db -U postgres mengxin -f /mnt/db.bak/data/mengxin/test.sql')
    print('{}合服数据导入完成{}'.format('\033[1;33m','\033[0m'))
    return True

if  __name__ == '__main__':
    try:
        if main():
            print('{0}脚本执行成功！！{}'.format('\033[1;33m','\033[0m'))
    except Exception , e :
        print('%s 萌新合服出现问题: %s，请检查%s' % ('\033[1;33m',e,'\033[0m'))



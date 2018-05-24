#!/usr/bin/env python
# coding:utf8

import paramiko
import sys
import threading
import os


# 此脚本需要在同一目录下存放hefu_server_list.txt文件
# hefu_server_list.txt存放需要合服的区服列表,需要合服的区服放在文件第一行
def get_text():
    new_list = []
    with open('hefu_server_list.txt', 'r') as f:
        for i in f.readlines():
            new_list.append(i.strip('\n'))
    return new_list


def remote_ssh(ip, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip)
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read())
    client.close()


def remote_exec(method, cmd):
    obj = []
    hefu_server_list = get_text()
    print(hefu_server_list)
    for host in hefu_server_list:
        t = threading.Thread(target=method, args=(host, cmd))
        obj.append(t)
    for t in obj:
        t.setDaemon(True)
        t.start()
    for t in obj:
        t.join()


def main():
    hefu_server_list = get_text()
    #    remote_exec(remote_ssh,'sudo /mnt/db.bak/xl/end_game.py')
    remote_exec(remote_ssh, 'pg_dump -h db -U postgres lyingdragon2 -f ~/$(hostname).sql')
    remote_ssh(hefu_server_list[0], 'pg_dump -h db -U postgres lyingdragon2 -sf ~/$(hostname).schema')
    remote_ssh(hefu_server_list[0], 'sudo cp ~/$(hostname).schema /var/lib/postgresql/lyingdragon.schema')
    remote_ssh(hefu_server_list[0], 'sudo cp /mnt/db.bak/xl/xiayang/wly_hefu_stage2.py ~/')
    for k, host in enumerate(hefu_server_list):
        if k != 0:
            os.system('scp {0}:~/wly-{0}.sql /home/xiayang/'.format(host))
            os.system('scp /home/xiayang/wly-{0}.sql {1}:~/'.format(host, hefu_server_list[0]))
            os.system('rm -f  /home/xiayang/wly-{0}.sql'.format(host))
        # remote_ssh(host,'sudo /mnt/db.bak/xl/shell_xl/changeHostname.sh debain')
        elif k == 0:
            os.system('scp hefu_server_list.txt {0}:~/'.format(host))


if __name__ == '__main__':
    try:
        main()
        print('卧龙吟初始化准备完毕，请到第一个区服上进行合服操作')
    except Exception as e:
        print('合服初始化脚本出现问题: %s，请检查' % e)


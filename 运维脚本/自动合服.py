#!/usr/bin/env python
# coding:utf8

import paramiko
import sys
import threading
import os

hefu_server_list = ['lequ-1006', 'lequ-1007', 'lequ-1008', 'lequ-1009']
port = 22
username = 'xiayang'
password = 'xiayang189'


def remote_ssh(ip, port, username, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username, password, timeout=4)
    stdin, stdout, stderr = client.exec_command(cmd)
    printstdout.read()
    client.close()


def remote_exec(cmd):
    obj = []
    for host in hefu_server_list:
        t = threading.Thread(target=remote_ssh, args=(host, port, username, password, cmd))
        obj.append(t)
    for t in obj:
        t.setDaemon(True)
        t.start()
    for t in obj:
        t.join()


def main():
    # remote_exec('sudo /mnt/db.bak/xl/end_game.py')
    remote_exec('pg_dump -h db -U postgres lyingdragon2 -f ~/$(hostname).sql')
    remote_ssh(hefu_server_list[0], port, username, password,
               'pg_dump -h db -U postgres lyingdragon2 -sf ~/$(hostname).schema')
    remote_ssh(hefu_server_list[0], port, username, password,
               'sudo cp ~/$(hostname).schema /var/lib/postgresql/lyingdragon.schema')
    for k, host in enumerate(hefu_server_list):
        if k != 0:
            os.system('scp {0}:~/wly-{0}.sql /home/xiayang/'.format(host))
            os.system('scp /home/xiayang/wly-{0}.sql {1}:~/'.format(host, hefu_server_list[0]))
            os.system('rm -f  /home/xiayang/wly-{0}.sql'.format(host))
            # os.system('sudo /mnt/db.bak/xl/shell_xl/changeHostname.sh debain')


if __name__ == '__main__':
    main()
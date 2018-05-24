#!/usr/bin/env python
# coding:utf8

import os
import socket

serverlist = {'wly':'lyingdragon2','xtw':'naughty','khbd':'dreamback','mycs':'naruto','mhjh':'legendary'}


def bak():
    a = os.popen('hostname')
    gamehostname = a.read().strip('\n')
    serverhead = gamehostname.split('-')[0]
    serverid = str(int(gamehostname.split('-')[2]))
    gamename = serverlist[serverhead]
    print('正在创建{}的目录'.format(gamehostname))
    os.system('sudo mkdir -pv /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}'.format(gamehostname))
    print('正在备份{}数据'.format(gamehostname))
    os.system('sudo pg_dump -h db -U postgres {} -f /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}.sql'.format(gamename,gamehostname))
    if serverhead == 'wly':
        print('正在拷贝wly配置文件')
        os.system('sudo cp /etc/conf/uqee/lyingdragon/server/config.json /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(gamehostname))
        os.system('sudo cp /home/soidc/wly_web/config/Servers{}.dat /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(serverid,gamehostname))
    elif serverhead == 'khbd':
        print('正在拷贝khbd配置文件')
        os.system('sudo cp /etc/conf/uqee/{}/server/config.json /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(gamename, gamehostname))
        os.system('sudo cp /home/soidc/khbd_web/config/Server.xml /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(gamehostname))
    elif serverhead == 'xtw':
        print('正在拷贝xtw配置文件')
        os.system('sudo cp /etc/conf/uqee/{}/server/config.json /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(gamename, gamehostname))
    elif serverhead == 'mycs':
        print('正在拷贝mycs配置文件')
        os.system('sudo cp /etc/conf/uqee/{}/server/config.json /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(gamename, gamehostname))
    elif serverhead == 'mhjh':
        print('正在拷贝mhjh配置文件')
        os.system('sudo cp /etc/conf/uqee/{}/server/config.json /mnt/db.bak/xl/xiayang/databak/reboot.server.bak/{}/'.format(gamename, gamehostname))


bak()
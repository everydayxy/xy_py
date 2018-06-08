#!/usr/bin/env python
# coding:utf8
import os
import datetime

file_path = '/opt/glog/'

game_list = ['bfxtw', 'dbtx', 'khbd', 'mhjh', 'naruto', 'wly']

uninclude_date = ['2018-05-14', '2018-05-13', '2018-05-12', '2018-05-11']


def get_serverid_path(file_path, game_list):  # 获取所有区服存放路径列表
    serverid_path = []
    for gamename in game_list:
        for serverid in os.listdir('{}/{}'.format(file_path, gamename)):
            serverid_path.append('{}{}/{}'.format(file_path, gamename, serverid))
    return serverid_path


def check(date):  # 检查日期是否合法
    y, m, d = date.split('-')
    try:
        datetime.date(int(y), int(m), int(d))
        return True
    except:
        return False


# print(serverid_path)
def get_date_path(serverid_path):  # 获取最近三天没有输出的区服日志保存路径
    date_path = []
    for path in serverid_path:
        try:
            date_list = os.listdir(path)
            if len(date_list) != 0:
                for date in date_list:
                    if not check(date):
                        break
                    if date in uninclude_date:
                        break
                    if path in date_path:
                        break
                else:
                    date_path.append('{}'.format(path))
        except:
            pass
    return date_path


# print uninclude_file_path

def move_log(uninclude_file_path):  # 移动日志
    print('cd /opt/glog/')
    for dir_path in game_list:
        print('mkdir /data/{}/'.format(dir_path))
    for path in uninclude_file_path:
        parts = path.split('/')
        print('mv {}/{} /data/{}/'.format(parts[3], parts[4], parts[3]))
        print('sleep 20')


if __name__ == '__main__':
    serverid_path = get_serverid_path(file_path, game_list)
    uninclude_file_path = get_date_path(serverid_path)
    move_log(uninclude_file_path)
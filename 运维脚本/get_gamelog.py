#!/usr/bin/env python
# coding:utf8
import os
import datetime
import time


def gethostlist(host):
    dirlist = os.listdir('/opt/glog/wly/')
    hostlist = []
    for ii in host:
        for i in dirlist:
            if ii in i:
                hostlist.append(i)

    return hostlist


def datelist(start_time, stop_time):
    begin_y, begin_m, begin_d = start_time.split('.')
    end_y, end_m, end_d = stop_time.split('.')
    ret = []
    begin = datetime.date(int(begin_y), int(begin_m), int(begin_d))
    end = datetime.date(int(end_y), int(end_m), int(end_d))
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        ret.append(str(day))

    return ret


def query(serveridlist, datelist):
    for serverid in serveridlist:
        new_dict = {}
        print(serverid)
        for date in datelist:
            path = '/opt/glog/wly/{}/{}/{}'.format(serverid, date, logname)
            #            print(path)
            try:
                with open(path, 'r') as f:
                    while True:
                        line = f.readline().strip('\n')
                        if len(line) == 0:
                            break
                        else:
                            parts = line.split('|')
                            dt = str(parts[2])
                            timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
                            timestamp = time.mktime(timeArray)
                            if int(timestamp) >= small_stamp1 and int(timestamp) <= small_stamp2:
                                if parts[1] in new_dict:
                                    new_dict[parts[1]][parts[3]] += int(parts[9])
                                else:
                                    new_dict[parts[1]] = {parts[3]: int(parts[9])}
            except:
                pass
        # print new_dict
        for i in new_dict:
            for ii in new_dict[i]:
                print
                i, ii, new_dict[i][ii]




if __name__ == '__main__':
    ##############################################################################
    # 以下为需要填写内容
    # 日志名称
    logname = 'GoldFlow.dat'
    # 日志开始/结束查询时间(精确到秒)
    when_start = '2018.03.01 04:00:00'
    when_stop = '2018.03.03 00:00:00'
    # 需要查询的服务器id
    host = ['wly-86-0571-hz-qq990-1024', 'wly-86-0571-hz-qq990-1030']
    # 日志开始查询时间(精确到天)
    start_time = when_start.split(' ')[0]
    # 日志结束查询时间(精确到天)
    stop_time = when_stop.split(' ')[0]
    # 日志开始查询时间(精确到秒)
    small_start_time = when_start
    # 日志结束查询时间(精确到秒)
    small_stop_time = when_stop
    ##############################################################################
    dt1 = str(small_start_time)
    timeArray = time.strptime(dt1, "%Y.%m.%d %H:%M:%S")
    small_stamp1 = time.mktime(timeArray)
    dt2 = str(small_stop_time)
    timeArray = time.strptime(dt2, "%Y.%m.%d %H:%M:%S")
    small_stamp2 = time.mktime(timeArray)


    datelist = datelist(start_time, stop_time)
    serveridlist = gethostlist(host)
    query(serveridlist, datelist)
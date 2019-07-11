#!/usr/bin/env python
# coding:utf8
import os
import datetime
import time
import salt.config
import salt.loader


def getgrains():
    minion_conf = salt.config.client_config('/etc/salt/minon')
    grains = salt.loader.grains(minion_conf)
    hostname = grains['localhost']
    return hostname


def gethostlist(start_time, stop_time):
    last_item = []
    datelists = datelist(start_time, stop_time)
    for dirlist in os.listdir('/var/log/lyingdragon/'):
        if dirlist in datelists:
            for item in os.listdir('{}{}'.format('/var/log/lyingdragon/',dirlist)):
                if item.endswith('.log'):
                    last_item.append('{}/{}/{}'.format('/var/log/lyingdragon',dirlist,item))

    return last_item


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


def main():
    hostname = getgrains()
    new_dict = {}
    host_file_list = gethostlist('2018.10.22','2018.10.29')
    for file in host_file_list:
        f = open('{}'.format(file),'r')
        for line in f:
            try:
                parts = line.split('|')
                dt = str(parts[3])
                timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
                timestamp = time.mktime(timeArray)
                if int(timestamp) >= 1540195200 and int(timestamp) <= 1540796400:
                    if parts[0] == 'GoldFlow':
                        parts = '{}|{}'.format(hostname,line).split('|')
                        if int(parts[12]) == 2:
                            if parts[3] in new_dict:
                                new_dict[parts[3]][-1] += int(parts[11])
                            else:
                                new_dict[parts[3]] = [parts[0], parts[5], int(parts[11])]
            except:
                pass
    for k, v in new_dict.items():
        if v[-1] > 6000:
            print '{},{},{},{}'.format(v[0], k, v[1], v[2])


if __name__ == '__main__':
    main()


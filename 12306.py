from urllib import request
import ssl
import sys
import json

ssl._create_default_https_context = ssl._create_unverified_context

def get_City_data():
# 获取城市代码
    url1 = request.urlopen('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9028')

    html1 = url1.read()

    html1 = html1.decode(encoding='utf-8')

    station_data = html1.split('=')[1].split('@')

    ret = {}

    for i in station_data:
        if '|' not in i:
            continue
        ret[i.split('|')[1]] = i.split('|')[2]

    return ret

def get_trains_info(date,from_station,to_station):
#查询火车信息方法实现
#https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT
    url2 = request.urlopen('https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station))

    html2 = url2.read()

    html2 = html2.decode(encoding='utf-8')

    return html2

def main(date,startcity,endcity):

    data = get_City_data()

    #print (data)

    info = get_trains_info(date,data[startcity],data[endcity])

    #print(info)
    if info.startswith(u'\ufeff'):
        info = info.encode('utf8')[3:].decode('utf8')


    hjson = json.loads(info)["data"]["result"]

    info_list = []

    for raw_train in hjson:
        # 循环遍历每辆列车的信息
        data_list = raw_train.split('|')
        # 车次号码
        train_no = data_list[3]
        # 出发站
        from_station_code = data_list[6]
        from_station_name = startcity
        # 终点站
        to_station_code = data_list[7]
        to_station_name = endcity
        # 出发时间
        start_time = data_list[8]
        # 到达时间
        arrive_time = data_list[9]
        # 总耗时
        time_fucked_up = data_list[10]
        # 一等座
        first_class_seat = data_list[31] or '--'
        # 二等座
        second_class_seat = data_list[30]or '--'
        # 软卧
        soft_sleep = data_list[23]or '--'
        # 硬卧
        hard_sleep = data_list[28]or '--'
        # 硬座
        hard_seat = data_list[29]or '--'
        # 无座
        no_seat = data_list[26]or '--'

        list = ('车次:{} 出发站:{} 目的地:{} 出发时间:{} 到达时间:{} 火车运行时间:{} 座位情况：\n 一等座：「{}」 二等座：「{}」 软卧：「{}」 硬卧：「{}」 硬座：「{}」 无座：「{}」\n\n'.format(train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))

        info_list.append(list)

    for i in info_list:
        print('*'*60)
        print (i)


a = str(input('请输入日期(格式“2010-10-10”)： '))
b = str(input('出发站： '))
c = str(input('到达站：'))


main(a,b,c)
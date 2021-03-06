import requests
import json

def get_City_data():
    '''
    城市代码获取
    '''
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9098'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
    response = requests.request('GET', url, headers=headers)
    html = response.text
    station_data = html.split('=')[1].split('@')
    ret = {}
    # unit :
    # 'zyi|遵义|ZYE|zunyi|zy|2844'
    for unit in station_data:
        if '|' not in unit:
            continue
        ret[unit.split('|')[1]] = unit.split('|')[2]
    return ret

def get_trains_info(date,from_station,to_station):
    '''
    火车信息查询方法函数
    '''
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
    response = requests.request('GET', url, headers=headers)
    html = response.text
    return html

def main(date,startcity,endcity):

    data = get_City_data()
    info = get_trains_info(date,data[startcity],data[endcity])
    hjson = json.loads(info)["data"]["result"]
    # raw_train:
    # "|预订|550000Z16420|Z164|SHH|LSO|SHH|LSO|20:08|19:30|47:22|N|SIygZtG7LXRkGXyeINjk7T5kNo40ywRzkHSmSiTp6MyIlkHIGPlTcQfsc9U%3D|20190303|3|H2|01|14|0|0||||无|||无||无|无|||||10401030|1413|0|0|null"
    for raw_train in hjson:
        # 循环遍历每辆列车的信息
        data_list = raw_train.split('|')
        # 车次号码
        train_no = data_list[3]
        # 出发站
        from_station_name = startcity
        # 终点站
        to_station_name = endcity
        # 出发时间
        start_time = data_list[8]
        # 到达时间
        arrive_time = data_list[9]
        # 总耗时
        time_used_up = data_list[10]
        # 一等座
        first_class_seat = data_list[31] or '--'
        # 二等座
        second_class_seat = data_list[30] or '--'
        # 软卧
        soft_sleep = data_list[23] or '--'
        # 硬卧
        hard_sleep = data_list[28] or '--'
        # 硬座
        hard_seat = data_list[29] or '--'
        # 无座
        no_seat = data_list[26] or '--'

        list = ('车次:{} 出发站:{} 目的地:{} 出发时间:{} 到达时间:{} 火车运行时间:{} 座位情况：\n 一等座：「{}」 二等座：「{}」 软卧：「{}」 硬卧：「{}」 硬座：「{}」 无座：「{}」'.format(train_no, from_station_name, to_station_name, start_time, arrive_time, time_used_up, first_class_seat,second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))

        print('*'*100)
        print(list)
        print('*'*100)


date = str(input('请输入日期(格式“2019-01-01”)： '))
startcity = str(input('出发站： '))
endcity = str(input('到达站：'))

if __name__ == '__main__':
    try:
        main(date,startcity,endcity)
    except KeyError:
        print('您输入的数据有问题，请重新输入')

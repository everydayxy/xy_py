#!/usr/bin/env python
# coding:utf8
import os


def get_text():
    new_list = []
    with open('hefu_server_list.txt','r') as f:
        for i in f.readlines():
            new_list.append(i.strip('\n'))
    return new_list


def main():
    hefu_server_list = get_text()
    version_num = str(raw_input('请输入wly合服脚本版本(格式为1.9.0): '))
    hefu_num = str(raw_input('请输入wly合服后区服号: '))
    version_num = version_num.replace('.', '_')
    hefu_new_list = ''
    hefu_len = len(hefu_server_list)
    count = 1
    for i in hefu_server_list:
        if count < hefu_len:
            hefu_new_list += 'wly-{}.sql,'.format(i)
            count+=1
        elif count == hefu_len:
            hefu_new_list += 'wly-{}.sql'.format(i)
    print('合服列表在此: %s' % hefu_server_list)
    print('合服版本在此: %s' % version_num)
    print('php脚本合服列表在此 %s' % hefu_new_list)
    os.system('cp /mnt/db.bak/data/new_comb_server_{}.php /home/xiayang/'.format(version_num))
    os.system('cd /home/xiayang/')
    os.system('sudo php new_comb_server_{0}.php comb wly{1} {2} > tmp.log'.format(version_num,hefu_num,hefu_new_list))
    return hefu_num

if __name__ == '__main__':
    try:
        hefu_num = main()
	print('合服成功,wly{}_bak文件为经过合并后的数据库，清检查'.format(hefu_num))
    except Exception as e :
        print('合服过程出现问题: %s，请检查' % e)



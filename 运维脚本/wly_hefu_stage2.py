#!/usr/bin/env python
# coding:utf8
import os


def get_text():
    new_list = []
    with open('hefu_server_list.txt','r') as f:
        for i in f.readlines():
            new_list.append(i.strip('\n'))
    return new_list

def tip(hefu_server_list):
        vstr = "{0}即将开始合服操作，请确认以上信息，1:继续,其它退出{1}"
        try:
            r = raw_input(vstr.format('\033[1;33m','\033[0m'))
            if len(r) ==  1 and r.isdigit() and int(r) == 1:
                return True
            return False
        except:
            print
            return False


def main():
    global hefu_num
    hefu_server_list = get_text()
    vstra = '{0}请选择需要哪种合服脚本：1 、大陆 2、越南：{1}'
    r = raw_input(vstra.format('\033[1;33m','\033[0m'))
    if r.isdigit() and int(r) == 1:
        hefuscriptforhead = 'new_comb_server'
    elif r.isdigit() and int(r) == 2:
        hefuscriptforhead = 'vn_new_comb_server'
    else:
        return False
    version_num = str(raw_input('{}请输入wly合服脚本版本(格式为1.9.0): {}'.format('\033[1;33m','\033[0m')))
    hefu_num = str(raw_input('{}请输入wly合服后区服号: {}'.format('\033[1;33m','\033[0m')))
    version_num = version_num.replace('.', '_')
    hefu_new_list = ''
    hefu_len = len(hefu_server_list)
    count = 1
    ret = []
    for i in hefu_server_list:
        ret.append('wly-{}.sql'.format(i))
#        if count < hefu_len:
#            hefu_new_list += 'wly-{}.sql,'.format(i)
#            count+=1
#        elif count == hefu_len:
#            hefu_new_list += 'wly-{}.sql'.format(i)
    hefu_new_list = ','.join(ret)
    print('%s合服列表在此: %s %s' % ('\033[1;33m',hefu_server_list,'\033[0m'))
    print('%s合服版本在此: %s %s' % ('\033[1;33m',version_num,'\033[0m'))
    print('%sphp脚本合服列表在此: %s %s' % ('\033[1;33m',hefu_new_list,'\033[0m'))
    if tip(hefu_server_list) is False:
        return False
    os.system('cp /mnt/db.bak/data/{}_{}.php ~/'.format(hefuscriptforhead,version_num))
    os.system('cd ~/')
    print('{}开始合服{}'.format('\033[1;33m','\033[0m'))
    os.system('sudo php {0}_{1}.php comb wly{2} {3} > tmp.log'.format(hefuscriptforhead,version_num,hefu_num,hefu_new_list))
    print('{}合服成功，正在将合服数据导入数据库{}'.format('\033[1;33m','\033[0m'))
    os.system('dropdb -h db -U postgres lyingdragon2 && createdb -h db -U postgres lyingdragon2 && psql -h db -U postgres lyingdragon2 -f ~/wly{}_bak'.format(hefu_num))
    return True

if __name__ == '__main__':
    try:
        if main():
            print('{0}合服成功,合服输出文件为wly{2}_bak{1}'.format('\033[1;33m','\033[0m',hefu_num))
    except Exception , e :
        print('%s合服过程出现问题: %s，请检查%s' % ('\033[1;33m',e,'\033[0m'))
#!/usr/bin/env python
# coding:utf8
import threading
import os
import argparse
import paramiko
import logging
# import salt.config
# import salt.loader
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class base():
    def __init__(self):
        '''
        获取脚本参数
        获取hostname
        定义日志参数
        '''
        args = self.arguments()
        self.hosts = args.hosts.split(',')
        self.version = args.version
        self.mergename = args.mergename if args.mergename else None
        try:
            self.num = int(args.local) if int(args.local) in (1,2) else None
        except TypeError:
            self.num = None
        self.version_num = self.version.replace('.', '_')
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S')
    def arguments(self):
        '''
        参数定义
        '''
        parse = argparse.ArgumentParser()
        parse.add_argument('-v', '--version', dest='version', help='游戏版本')
        parse.add_argument('-hosts', '--hosts', dest='hosts', help='游戏合服列表')
        parse.add_argument('-l', '--local', dest='local', help='游戏地理位置')
        parse.add_argument('-n','--mergename',dest='mergename',help='游戏最终合服名字')
        args = parse.parse_args()
        return args
    def remote_ssh(self,ip, cmd):
        '''
        远程ssh方法
        '''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip)
        stdin, stdout, stderr = client.exec_command(cmd)
        st = stdout.read()
        ste = stderr.read()
        logging.info(st)
        logging.error(ste)
        client.close()
        return
    def remote_exec(self,method, cmd):
        '''
        获取游戏列表并批量执行命令
        '''
        obj = []
        logging.info('执行的区服列表:{}'.format(self.hosts))
        for host in self.hosts:
            t = threading.Thread(target=method, args=(host, cmd))
            obj.append(t)
        for t in obj:
            t.start()
        for t in obj:
            t.join()
        return
    def shutdown(self):
        '''
        1.关服
        2.导出数据到堡垒机
        3.修改首服之后的名字为debain
        '''
        shutdown_game = 'sudo /mnt/db.bak/xl/end_game.py'
        dump_db = 'sudo pg_dump -h db -U postgres lyingdragon2 -f /mnt/db.bak/data/wly/$(hostname).sql'
        change_hostname_debain = 'sudo /mnt/db.bak/xl/shell_xl/changeHostname.sh debain'
        logging.info('开始关闭区服')
        # 执行shell
        #self.remote_exec(self.remote_ssh,shutdown_game)
        logging.info('区服关闭成功')
        logging.info('正在导出各个区服数据库')
        # 执行shell
        self.remote_exec(self.remote_ssh,dump_db)
        logging.info('各个区服数据库导出完成')
        for idx, host in enumerate(self.hosts):
            if idx != 0:
                logging.info('正在修改{}服的名字为debain'.format(host))
                # 执行shell
                #self.remote_ssh(host,change_hostname_debain)
                logging.info('{}服的名字修改完成'.format(host))
        return True
    def merge(self):
        '''
        1.复制数据库表结构
        2.合服
        '''
        db_dump_schema = 'sudo pg_dump -h db -U postgres lyingdragon2 -sf /mnt/data/data/wly/lyingdragon.schema'
        cp_dump_schema = 'sudo cp /mnt/data/data/wly/lyingdragon.schema /var/lib/postgresql/lyingdragon.schema'
        if not self.mergename:
            self.mergename = raw_input('请输入合服名字(区服名字全称,比如wly-lehh-1010): ')
        logging.info('合服区服名字为{}'.format(self.mergename))
        logging.info('合服版本号为{}'.format(self.version))
        logging.info('开始合服')
        logging.info('开始合服')
        # 执行shell
        print('{4} && {5} &&  cd /mnt/data/data/wly/ && sleep 3 && sudo php {0}_{1}.php comb wly{2} {3} > tmp.log'.format(
            self.hefuscriptforhead,
            self.version_num,
            self.mergename.split('-')[-1],
            ','.join(self.hosts),
            db_dump_schema,
            cp_dump_schema
        ))
        logging.info('合服结束')
        return True
    def picklocation(self):
        '''
        1.选择脚本前缀
        2.判断合服脚本是否存在
        '''
        if self.num:
            if self.num == 1:
                self.hefuscriptforhead = 'new_comb_server'
            elif self.num == 2:
                self.hefuscriptforhead = 'vn_new_comb_server'
        else:
            vstra = '{0}请选择需要哪种合服脚本：1 、大陆 2、越南：{1}'
            r = int(raw_input(vstra.format('\033[1;33m', '\033[0m')))
            if r == 1:
                self.hefuscriptforhead = 'new_comb_server'
            elif r == 2:
                self.hefuscriptforhead = 'vn_new_comb_server'
            else:
                logging.error('您选择的东西不支持，退出')
                sys.exit(1)
        if not os.path.isfile('/mnt/data/data/{}_{}.php'.format(self.hefuscriptforhead, self.version_num)):
            logging.error('合服脚本不存在，请检查！！！')
            sys.exit(1)
        else:
            # 执行shell
            print('sudo cp {} {}'.format(
                '/mnt/data/data/{}_{}.php'.format(self.hefuscriptforhead, self.version_num),
                '/mnt/data/data/wly/'))
        return True
    def changeconfig(self):
        logging.info('正在修改游戏配置文件')
        # 执行shell
        #self.remote_ssh(self.hosts[0], 'sudo /mnt/db.bak/xl/xiayang/kaifu.py')
        logging.info('游戏配置文件修改完成')
        return True
    def dboperate(self):
        dropdb = 'dropdb -h db -U postgres lyingdragon2'
        createdb = 'createdb -h db -U postgres lyingdragon2'
        psql = 'psql -h db -U postgres lyingdragon2 -f /mnt/data/data/wly/wly{}_bak > /dev/null'
        cmd1 = ('{} && {} && {}'.format(dropdb,createdb,psql.format(self.mergename.split('-')[-1])))
        print(cmd1)
        # 执行shell
        #self.remote_ssh(self.hosts[0],cmd1)
        return True
    def main(self):
        logging.info('开始合服操作')
        flag = False
        if self.shutdown():
            if self.picklocation():
                if self.merge():
                    if self.dboperate():
                        if self.changeconfig():
                            logging.info('合服操作结束')
                            flag = True
        if flag is not True:
            logging.error('脚本还没执行完就退出了')
if __name__ == '__main__':
    Base = base()
    Base.main()


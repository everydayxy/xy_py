# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
import os,socket,json,urllib2,time,sys
from random import randint
import psutil,json,types
import shutil
import salt.utils
import logging
reload(sys)
sys.setdefaultencoding("utf-8")
log = logging
__virtualname__ = "uqee_game"

config_file = os.path.dirname(__file__) + "/gameinfo.conf"
def __virtual__():
    return __virtualname__ if os.path.isfile(config_file) else False


class base(object):
    ret = {"result": False,"error": "此服务器不支持该操作",
           "comment":["此服务器不支持该操作"]}
    def getServerInfo(self):
        return self.ret
    def getAdminAddr(self):
        return self.ret
    def setConfig(self):
        return self.ret
    def rollBack(self):
        return self.ret



    def cleandb(self,*args,**kwargs):
        ret = {'result':False,'desc':""}
        game_server_type = __grains__.get('game_server_type',1)
        gameinfo = self._getConfig()
        log.info('开始清档');
	log.info('--------------')
        server_list = __grains__.get('server_list',[]);
        log.info('list:{}'.format(server_list))
	dbname = self.dbname
	log.info('dbname:{}'.format(dbname))
        if game_server_type == 2 : 
            if not kwargs.get('server_id'):
                ret['desc'] = '请指定需要清档的服务器'
                return ret
            for item in server_list:
                if item['server_id'] == kwargs.get('server_id'):
                    server = item;
                    dbname = item['dbname']
                    break
            else:
                ret['desc'] = '指定服务器不在服务器列表中'
                return ret;
            pid = self._getPidByPort(server['sock_port'])
        else:
            pid = self._getPid(self.gamename);
        if pid:
            self.shutgame(server_id=kwargs.get('server_id',None))
        result,desc = self._clean_postgresql(dbname,kwargs.get('no_save'))
        ret['result'] = result
        ret['desc'] = desc;
        if result is False:
            return ret
        res = self.startgame(server_id=kwargs.get('server_id',None))
        if res['result'] is not True:
            ret['desc'] += ',游戏开启失败,请手动开启'
        ret['comment'] = res['comment']
        return ret

    def _clean_postgresql(self,dbname=None,state=None):
        '''
        清档内容
        '''
        config = self._getConfig()
        rec = ['psql -h db -U postgres'] #还原
        dump = ["pg_dump -h db -U postgres"]  #备份
        reCmd = ['invoke-rc.d postgresql restart'] #重启
        if dbname is None:
            dbname = config.get(self.gamename,'dbname')
        dump.append(dbname)
        rec.append(dbname)
        drop = ['dropdb -h db -U postgres',dbname]  #删除数据库
        create = ['createdb -h db -U postgres',dbname] #创建数据库
        baktables = config.get(self.gamename,'baktables')
        if len(baktables):
            baktables = baktables.split(',')
        else:
            baktables = list()
        if state is True:
            nobaktb = config.get(self.gamename,'nobaktb')
            baktables.remove(nobaktb)
        bakFilePath = "/var/lib/postgresql"
        bakFile = os.path.join(\
            bakFilePath,\
                "{0}_{1}.bak".format(dbname,time.strftime('%Y-%m-%d_%H:%M:%S')))
        schema = os.path.join(\
            bakFilePath,\
                "{0}_{1}.schema".format(dbname,time.strftime('%Y-%m-%d_%H:%M:%S')))
        psql = list()
        psql.append(dump + ["-f"] + [bakFile]) #备份数据库
        psql.append(dump + ["-sf"] + [schema]) #备份结构表
        for table in baktables:  #备份保留的表
            psql.append(dump + ["-t"] + [table] + ["-af"] + \
                            [os.path.join(bakFilePath,"{0}.bak".format(table))])
        # psql.append(reCmd)  #重启数据库
        psql.append(drop) #删除表
        psql.append(create)  #创建表
        psql.append(rec + ["-f"] + [schema])  #还原表结构
        for table in baktables:
            psql.append(rec + ["-f"] +\
                            [os.path.join(bakFilePath,"{0}.bak".format(table))])
        if config.has_option(self.gamename,'sql'):  #要执行的SQL
            for sql in config.get(self.gamename,'sql').split("@"):
                psql.append(rec + ["-c"] + ['"{0}"'.format(sql)])
        for cmd in psql:
            log.error(" ".join(cmd))
            ret =  __salt__['cmd.run_all'](" ".join(cmd))
            if ret['retcode'] != 0:
                return (False,ret['stderr'])

        return (True,'清档成功')

    def _create_fork_upload_databak(self,*args,**kwargs):
        waittime = randint(1,1800)
        log.info('上传文件等待{0}秒'.format(waittime))
        newpid = os.fork()
        if newpid == 0:
            time.sleep(waittime)
            os.setsid()
            mysocket(*args)
            sin = file('/dev/null','r')
            sout = file('/dev/null','a+')
            serr = file('/dev/null','a+',0)
            sys.stdout.flush()
            sys.stderr.flush()
            os.dup2(sin.fileno(),sys.stdin.fileno())
            os.dup2(sout.fileno(),sys.stdout.fileno())
            os.dup2(serr.fileno(),sys.stderr.fileno())
        else:
            pass


    def _getConfigJson(self,json_file=None):
        if json_file is None:
            json_file = "/etc/conf/uqee/%s/server/config.json"%(self.gamepath,)
        if os.path.isfile(json_file):
            file_content=open(json_file,'r')
            json_centent=json.load(file_content,encoding='utf8')
            try:
                domain=json_centent['server']['report']['address']
            except KeyError:
                try:
                    domain=json_centent['server']['host']
                except KeyError:
                    domain = ''
            serverid=json_centent['server']['id']
            eths = json_centent['server']['sock']['eth'].split(';')
            return [domain,serverid,eths]
        else:
            return [False,False,False]

    def databak(self,*args,**kwargs):
        game_server_type = __grains__.get('game_server_type',1)
        log.info('-' * 50)
        log.info('服务器类型:{0}'.format(game_server_type))
        if game_server_type == 1:
            return self.databak_single(*args,**kwargs)
        elif game_server_type==2:
            return self.databak_multiple(*args,**kwargs)


    def databak_multiple(self,*args,**kwargs):
        ret = {'result':True,'comment':list()}
        server_list = __grains__.get('server_list',[])
        if len(server_list) == 0:
            return ret
        for item in server_list:
            json_file = os.path.join(item['work_dir'],self.gamename,'config.json')
            log.info('正在备份区服:{0},数据库:{1}'.format(item['server_name'],item['dbname']))
            dbname = item['dbname']
            r = self.databak_single(dbname=dbname,json_file=json_file)
            ret['comment'].append(r['desc'])
        return ret


    def databak_single(self,*args,**kwargs):
        ret = {'result':True,'desc':"备份成功"}
        # 设置MTU
        __salt__['cmd.run']("/sbin/ifconfig eth1 mtu 1496")
        domain,serverid,eths = self._getConfigJson(kwargs.get('json_file',None))
        if domain is False:
            log.error('get config.json info error')
            ret['result'] = False
            ret['desc'] = 'config.json文件配置错误, domain为空'
            return ret
        if __salt__['network.ipaddrs'](eths[0]).__len__() !=0:
            domain = __salt__['network.ipaddrs'](eths[0])[0]
        else:
            domain = __salt__['network.ipaddrs'](eths[1])[0]
        wday = time.strftime('%w')
        hour = int(time.strftime('%H'))
        data_dir = '/mnt/data/datacenter/%s/' % self.gamename
        data_dir=os.path.join(data_dir,serverid)
        file_dir='/var/lib/postgresql/%s' % serverid
        if not os.path.isdir(file_dir):
            log.info('文件夹{0}不存在,开始创建'.format(file_dir))
            os.makedirs(file_dir)
        dbname = kwargs.get('dbname',self.dbname)
        file_name = "%s_%s_%s_%s.bak.gz" %(self.gamename,
            wday,hour,domain)
        log.info('备份文件名:{0}'.format(file_name))
        bakfilename = os.path.join(file_dir,file_name)
        log.info('备份文件完整路径:{0}'.format(bakfilename))
        cmd = "pg_dump -h db -U postgres -Z9 %s -f %s" %(dbname,bakfilename)
        if self.gamename == 'card':
            file_dir='/var/lib/data/mongodb/%s' % serverid
            if not os.path.isdir(file_dir):
                log.info('文件夹{0}不存在,开始创建'.format(file_dir))
                os.makedirs(file_dir)
            file_name = '%s_%s_%s_%s'%(self.gamename,
                wday,hour,domain)
            cmd = "/var/lib/mongodb/bin/mongodump -u admin -p soidc..123 -d %s -o %s" %\
                (dbname,file_dir)
            bakfilename = os.path.join(file_dir,file_name)
            if os.path.exists(bakfilename):
                log.info('历史文件存在,删除!')
                shutil.rmtree(bakfilename)
        env = {'LC_ALL':'en_US.UTF-8'}
        res = __salt__['cmd.run_all'](cmd,shell="/bin/bash", env=env)
        if res['retcode'] !=0:
            log.error('备份失败,备份命令:%s' % cmd)
            ret['result'] = False
            ret['desc'] = 'do dump database %s error' % dbname
            return ret
        if self.gamename == 'card' and \
        os.path.isdir(os.path.join(file_dir,self.gamename)):
            os.rename(os.path.join(file_dir,self.gamename),bakfilename)
            shutil.copy('/var/lib/redis/appendonly.aof',os.path.join(bakfilename,'appendonly.aof'))
        tar_name="%s_%s_%s.tar.gz"%(self.gamename,wday,hour)
        tarfilename = os.path.join(file_dir,tar_name)
        log.info('压缩文件:{0}'.format(tarfilename))
        res = __salt__['archive.tar']('zcf',tarfilename,file_name,None,file_dir)
        self._create_fork_upload_databak(tarfilename,os.path.join(data_dir,tar_name))
        log.info('创建子进程序,数据库名:{0}'.format(dbname))
        if hour not in [1,4]:
            __salt__['file.remove'](bakfilename)
        return ret

    def _getPidByPort(self,port):
        pid = None
        for process in psutil.process_iter():
            conn = process.get_connections();
            for c in conn:
                if c.status == 'LISTEN' and c.local_address[1] == port:
                    pid = process.pid
                    break
        return pid



    def _getPid(self,name,user=None):
        for process in psutil.process_iter():
            if process.name == name:
                if user:
                    if process.user == user:
                        return process.pid
                    else:
                        return None
                return process.pid
        else:
            return None

    def doSth(self,host,port,command,**kwargs):
        ret = {'code':True,'desc':''}
        conn  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((host,port))
        except Exception as e:
            log.error("Connection {0}:{1} failed".format(host,port))
            ret['code'] = False;
            ret['desc'] = '连接游戏服务器失败'
            return ret;
        conn.sendall(command)
        while True:
            data = conn.recv(4096)
            if data == "":
                break
            ret['desc'] += str(data)
        return ret

    def installGame(self,*args,**kwargs):
        keys = kwargs.keys()
        env = {'LC_ALL':'en_US.UTF-8'}
        ret = {'result':True,'desc':""}
        if 'alias' not in keys:
            ret['result'] = False
            ret['desc'] = "alias is not exists"
            return ret
        if 'hostname' not in keys:
            ret['result'] = False
            ret['desc'] = 'hostname is not exists'
            return ret
        ssl = 1 if kwargs['ssl'] == '1' else 0
        player_state = 1 if kwargs['log'] != '0' else 0
        preask = 1 if kwargs['preask'] != '0' else 0
        gname = __salt__['pillar.get']("game:gamename")
        __salt__['saltutil.sync_all']()
        __salt__['saltutil.refresh_pillar']()
        __salt__['grains.setval']('gamepackage','game-init')
        __salt__['grains.setval']('prev',kwargs['alias'])
        __salt__['grains.setval']('server_version',kwargs['version'])
        __salt__['uqee_chkgame.hostname'](kwargs['hostname'])
        __salt__['grains.setval']('localhost',kwargs['hostname'])
        __salt__['grains.setval']('gamename',gname)
        __salt__['grains.setval']('ssl',ssl)
        __salt__['grains.setval']('player_state',player_state)
        __salt__['grains.setval']('preask',preask)
        log.info('start install')
        r = __salt__['uqee_chkgame.checkgame']()
        if r is not False:
            ret['result'] = False
            ret['desc'] = r
            return ret
        actions = ['system','pam','game.postgresql','game.cron','game.web','game.report','game.game',
            'game.player_state','nagios','game.zabbix','game.after','system.updategrains']
        if gname == 'card':
            actions.insert(actions.index('game.game'),'game.mongodb')
        ret['desc'] = list()
        for action in actions:
            if action == 'system' and __salt__['grains.get']('install_system'):
                action = 'system.iptable'
            if action == 'pam' and __salt__['grains.get']('install_pam'):
                continue
            log.info(action)
            result = __salt__['state.sls'](action)
            # print(type(ret))
            succ = True
            for key,value in result.items():
                if value['result'] is not True:
                    ret['desc'].append(json.dumps(value))
                    succ = False
            if action == 'pam' and succ:
                __salt__['grains.setval']('pam_install',True)
        return ret


    def _checkLogAndStore(self,configfile):
        '''
        查看游戏的配置,检查是不是否日志和战报中心
        @return dict  返回启用情况
        '''
        ret = {'code':True,"desc":""}
        # configfile = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        if not os.path.isfile(configfile):
            ret['code'] = False
            ret['desc'] = '游戏配置文件不存在:'+configfile
            return ret;
        configCentent = json.load(open(configfile,"r"),encoding="UTF-8")
        ret['sid'] = configCentent['server']['id']
        if configCentent['game']['log'].has_key('tcp'):
            logAddr = configCentent['game']['log']['tcp'].get('center')
            if logAddr :
                ret['log'] = 'foxlog'
        if configCentent.has_key('store'):
            batt = configCentent.get('store').get('address')
            if batt :
                ret['store'] = 'foxstorage'
        return ret

    def _getGameFileList(self):
        '''
        返回当前游戏要开启的程序
        '''
        config = self._getConfig()
        gameFileList = list()
        gameFileList.append('foxlog')
        if config.getboolean(self.gamename,'foxstorage'):
            gameFileList.append('foxstorage')
        if config.getboolean(self.gamename,'memcache'):
            gameFileList.append('memcache')
        if config.has_option(self.gamename,'other'):
            gameFileList += config.get(self.gamename,'other').split(',')
        gameFileList.append(self.gamename)
        return gameFileList


    def _getIP(self,jsonFile=None):
        config = self._getConfig()
        if jsonFile == None:
            jsonFile = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        if not os.path.isfile(jsonFile):
            return dict()
        jsonStr = json.load(open(jsonFile,"r"))
        ret = dict();
        ret['ipaddr'] = __grains__.get('ipv4',[])
        ret['server_id'] = jsonStr['server']['id']
        ret['server_name'] = jsonStr['server']['name']
        return ret

    def _getConfig(self):
        config = SafeConfigParser()
        if config_file:
            log.error(config_file)
            with open(config_file,"r") as _fp:
                config.readfp(_fp)
        return config


    def doHttp(self,url,method,**kwargs):
        ret = {'code':True,'desc':''}
        if 'username' in kwargs.keys() and \
            'password' in kwargs.keys() and\
            kwargs['username'] and kwargs['password']:
            username = kwargs['username']
            password = kwargs['password']
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None,url,username,password)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
        data = None
        if method == "POST":
            data = kwargs['data']
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req,data,1200);
            if res.code == 200:
                return ret
            else:
                ret['code'] = False
                ret['desc'] = '访问URL:'+ url + "失败,http_code:"+ ret.code;
                return ret
        except Exception as e:
            print e
        else:
            pass
        finally:
            pass
        

    def shutgame(self,*args,**kwargs):
        game_server_type = __grains__.get('game_server_type',1)
        if game_server_type == 1:
            return self.shutgame_single(*args,**kwargs)
        elif game_server_type ==2:
            shut_all = kwargs.get('shut_all')
            if shut_all:
                ret = {"result": True,"comment": dict()}
                msg = list()
                server_list = __grains__.get('server_list')
                for item in server_list:
                    kwargs['server_id'] = item['server_id']
                    r =  self.shutgame_multiple(*args,**kwargs)
                    msg.append("{0}:{1}".format(item['server_name'],"\n".join(r['comment'])))
                ret['comment'] = {"message":"\n".join(msg)}
                return ret
            else:
                return self.shutgame_multiple(*args,**kwargs)

    def shutgame_multiple(self,*args,**kwargs):
        ret = {"result": False,
               "comment": list()}
        server_list = __grains__.get('server_list')
        if len(server_list) == 0:
            ret['comment'].append('还没有配置区服')
            return ret
        if not kwargs.has_key('server_id'):
            ret['comment'].append('请指定需要开的服务器ID')
            return ret
        server = []
        for item in server_list:
            if item['server_id'] == kwargs['server_id']:
                index = server_list.index(item)
                server = item
                break
        else:
            ret['comment'].append('需要开启的服务器不在已配置的区服中')
            return ret
        # 关掉通知
        server_list[index]['is_notify'] = False
        __salt__['grains.setval']('server_list',server_list)
        config = self._getConfig()
        processes = config.get(self.gamename,'shutgame_process')
        try:
            processes = eval(processes)
        except:
            ret['comment'].append('配置有误')
            return ret;


        sleep_time = kwargs.get('sleep_time',5)

        for process in processes:
            pid = self._getPidByPort(server['sock_port']);
            flush = False
            if pid is None:
                ret['comment'].append('游戏进程{0}没有开启'.format(process['name']))
                continue
            if 'flush' in process.keys():
                flush = process['flush']
            if 'host' not in process.keys():
                host = self.ip
            else:
                host = process['host'];

            if process['command'] is None and \
                pid is not None:
                __salt__['ps.kill_pid'](pid,9)
                continue
            if process['method'] == 'socket':
                sh_ret = self.doSth(host,server['console_port'],process['command']);
            elif process['method'] == 'http':
                host = self._getIpByPort(server['admin_port'])
                url = process['command'].format(ip=host,port=server['console_port'])
                username = process['username'] if process.has_key('username') else None
                password = process['password'] if process.has_key('password') else None
                sh_ret = self.doHttp(url,process['http_method'],data="1",username=username,password=password)
            if sh_ret['code'] is not True:
                desc = process['name'] + ":" + sh_ret['desc']
                ret['comment'].append(desc);
            time.sleep(sleep_time)
            if self._getPidByPort(server['sock_port']) is not None and flush is False:
                desc = "程序:{0},没有正常关闭,强制关闭!".format(process['name'])
                ret['comment'].append(desc)
                time.sleep(10)
                __salt__['ps.kill_pid'](pid,9)
            if flush is False:
                ret['comment'].append('程序:{0},已关闭'.format(process['name']));
        ret['result'] = True
        return ret


    def shutgame_single(self,*args,**kwargs):
        '''
        关闭游戏,
        '''
        ret = {"result": True,
               "comment": list()}
        __salt__['grains.setval']('is_notify',False)
        config = self._getConfig()
        processes = config.get(self.gamename,'shutgame_process')
        try:
            processes = eval(processes)
        except:
            ret['comment'].append('配置有误')
            ret['result'] = False
            return ret;
        sleep_time = kwargs.get('sleep_time',5)
        for process in processes:
            pid = self._getPid(process['name']);
            if pid is None:
                desc = "程序:{0}进程不存在 ".format(process['name']);
                ret['comment'].append(desc);
                continue;
            flush = False
            if 'flush' in process.keys():
                flush = process['flush']
            if 'host' not in process.keys():
                host = self.ip
            else:
                host = process['host'];

            if process['command'] is None and \
                pid is not None:
                __salt__['ps.kill_pid'](pid,9)
                continue
            if process['method'] == 'socket':
                sh_ret = self.doSth(host,process['port'],process['command']);
            elif process['method'] == 'http':
                host = self._getIpByPort(process['port'])
                url = process['command'].format(ip=host,port=process['port'])
                username = kwargs['username'] if kwargs.has_key('username') else  process.get('username',None);
                password = kwargs['password'] if kwargs.has_key('password') else  process.get('password',None);
                sh_ret = self.doHttp(url,process['http_method'],data="1",username=username,password=password)
            if sh_ret['code'] is not True:
                desc = process['name'] + ":" + sh_ret['desc']
                ret['comment'].append(desc);
            time.sleep(sleep_time)
            while True:
                if self._getPid(process['name']) is not None and flush is False:
                    desc = "程序:{0},没有正常关闭,强制关闭!".format(process['name'])
                    ret['comment'].append(desc)
                    __salt__['ps.kill_pid'](pid,9)
                    time.sleep(10)
                else:
                    break;
            if flush is False:
                ret['comment'].append('程序:{0},已关闭'.format(process['name']));
        return ret

    def _checkRun(self,name,user):
        '''
        检查即将要开启的这个程序是不是已经在运行了
        '''
        ret = True
        for process in psutil.process_iter():
            if process.name == name:
                break
        else:
            return False
        return ret


    def startgame(self,*args,**kwargs):
        game_server_type = __grains__.get('game_server_type',1)
        if game_server_type == 1:
            return self.startgame_single(*args,**kwargs)
        if game_server_type == 2:
            start_all = kwargs.get('start_all')
            if start_all:
                ret = {"result": True,"comment": dict()}
                msg = list()
                server_list = __grains__.get('server_list')
                for item in server_list:
                    kwargs['server_id'] = item['server_id']
                    r =  self.startgame_multiple(*args,**kwargs)
                    msg.append("{0}:{1}".format(item['server_name'],r['comment'].get('message')))
                ret['comment'] = {"message":"\n".join(msg)}
                return ret
            else:
                return self.startgame_multiple(*args,**kwargs)


    def startgame_multiple(self,*args,**kwargs):
        ret = {"result": False,"comment": dict()}
        server_list = __grains__.get('server_list')
        if len(server_list) == 0:
            ret['comment'].update({'message': '还没有配置区服'})
            return ret
        if not kwargs.has_key('server_id'):
            ret['comment'].update({'message':'请指定需要开的服务器ID'})
            return ret
        server = []
        for item in server_list:
            if item['server_id'] == kwargs['server_id']:
                server = item
                break
        else:
            ret['comment'].update({'message':'需要开启的服务器不在已配置的区服中'})
            return ret
        game_config = os.path.join(server['work_dir'],self.gamename,'config.json')
        chkgame = self._checkLogAndStore(game_config)
        gameFileList = self._getGameFileList()
        if chkgame['code'] is False:
            ret['result'] = False
            ret['comment'].update({'message':chkgame['desc']});
            return ret
        if chkgame.get('log'):
            gameFileList.remove(chkgame['log'])
        if chkgame.get('store'):
            gameFileList.remove(chkgame['store'])
        os.environ['log_stdout'] = '1'
        os.environ['config_file'] = game_config
        env = {'LC_ALL':'en_US.UTF-8'}
        gameinfo_config = self._getConfig()
        waittime = 5
        if gameinfo_config.has_option(self.gamename,'waittime'):
            waittime = int(gameinfo_config.get(self.gamename,'waittime'))
        for pathfile in gameFileList:
            game_file = os.path.join(server['work_dir'],pathfile,pathfile)
            cmd = "screen -mdS {0} ./{1}".format(os.path.basename(server['work_dir']),pathfile)
            if not os.path.isfile(game_file):
                ret['comment'].update({'message': game_file+ '文件不存在'})
                log.warning("{0} is not exists".format(game_file))
                return ret
            port = server['sock_port']
            pid = self._getPidByPort(port);
            if pid:
                ret['comment'].update({'message': pathfile + '已经在运行,跳过'})
                log.warning("{0} already running,Skip!".format(pathfile))
                return ret
            work_cwd = os.path.join(server['work_dir'],pathfile)
            startRet = __salt__['cmd.run_all'](cmd,cwd=work_cwd,shell="/bin/bash",env=env)
            if startRet['retcode'] == 0:
                ret['comment'].update({'message' : "{0}:开启成功,请确认.".format(pathfile)})
            else:
                ret['result'] = False
                ret['comment'].update({'message' : "{0}:开启失败,请让运维同事查看.".format(pathfile)})
                log.error("{0} was started failed!".format(pathfile))
                return ret
            time.sleep(waittime)
        if kwargs.get('notify_state',True) is not False:
            index = server_list.index(server)
            server['is_notify'] = True
            server_list[index] = server
            __salt__['grains.setval']('server_list',server_list)
        ret['result'] = True
        return ret


    def startgame_single(self,*args,**kwargs):
        '''
        开启游戏
        '''
        ret = {"result": True,"comment": dict()}
        game_config = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        chkgame = self._checkLogAndStore(game_config)
        gameFileList = self._getGameFileList()
        if chkgame['code'] is False:
            ret['result'] = False
            ret['comment'].update({'config_file':chkgame['desc']});
            return ret
        if chkgame.get('log'):
            gameFileList.remove(chkgame['log'])
        if chkgame.get('store'):
            gameFileList.remove(chkgame['store'])
        os.environ['log_stdout'] = '1'
        env = {'LC_ALL':'en_US.UTF-8'}
        gameinfo_config = self._getConfig()
        waittime = 5
        if gameinfo_config.has_option(self.gamename,'waittime'):
            waittime = int(gameinfo_config.get(self.gamename,'waittime'))
        for pathfile in gameFileList:
            if pathfile == "lyingdragon":
                path = "/root/workspace/{0}/{0}".format(pathfile)
            else:
                path = "/root/workspace/{0}".format(pathfile)
            cmd = "screen -mdS {0} ./{0}".format(pathfile)
            if self._checkRun(pathfile,'root'):
                ret['comment'].update({pathfile: "已经在运行,跳过"})
                log.warning("{0} already running,Skip!".format(pathfile))
                continue
            if not os.path.exists(os.path.join(path,pathfile)):
                ret['comment'].update({os.path.join(path,pathfile): "文件不存在,请注意"})
                log.warning("{0} is not exists".format(pathfile))
                ret['result'] = False
                continue
            startRet = __salt__['cmd.run_all'](cmd,cwd=path,shell="/bin/bash",env=env)
            if startRet['retcode'] == 0:
                ret['comment'].update({pathfile : "开启成功,请确认."})
            else:
                ret['result'] = False
                ret['comment'].update({pathfile : "开启失败,请让运维同事查看."})
                log.error("{0} was started failed!".format(pathfile))
                return ret
            time.sleep(waittime)
        if kwargs.get('notify_state',True) is not False and __grains__.get('is_notify',False) is False:
            __salt__['cmd.run']('echo "salt-call grains.setval is_notify True" | /usr/bin/at NOW + 3min',shell='/bin/bash',runas='root')
        return ret

    def _getIpByPort(self,port=None):
        ipaddr = '127.0.0.1'
        for process in psutil.process_iter():
            conn = process.get_connections();
            for c in conn:
                if c.status == 'LISTEN' and c.local_address[1] == port:
                    ipaddr = c.local_address[0]
                    if ipaddr == '127.0.0.1':
                        continue
                    break
        return ipaddr

    def _socketMonitorCheck(self,host,port,command,*args,**kwargs):
        ret = {"result":False,"desc": "","exitCode":0}
        socket.setdefaulttimeout(10)
        cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if command is None:
            command = '@'
        try:
            cs.connect((host,port))
            cs.send(command)
            data = cs.recv(1024)
            log.info("{0} is ok now!".format(kwargs['name']))
            ret['desc'] = "{0} is ok now!".format(kwargs['name'])
            ret['result'] = True
            ret['exitCode'] = 0
        except socket.timeout as e:
            log.warning("{0} was stopped!, cause: {1}".format(kwargs['name'],str(e)))
            ret['exitCode'] = 1
            ret['desc'] = "{0} was stopped!, cause: {1}".format(kwargs['name'],str(e))
        except socket.error as e:
            ret['exitCode'] = 2
            log.error("{0} was stopped!, cause: {1}".format(kwargs['name'],str(e)))
            ret['desc'] = "{0} was stopped!, cause: {1}".format(kwargs['name'],str(e))

        finally:
            cs.close()
        return ret

    def monitorBase(self,*args,**kwargs):
        ret = {"result":False,"desc": [],"exitCode":0}
        exitCode = 0
        if not kwargs.has_key('check_list'):
            ret['desc'] = 'check list is empty'
            return ret
        check_list = kwargs.get('check_list')
        for item in check_list:
            if item.get('host') is None:
                item['host'] = self._getIpByPort(item['port'])
            if item['method'] == 'http':
                pass
            else:
                r = self._socketMonitorCheck(item['host'],item['port'],item['command'],name=item['name'])
                if r['exitCode'] > exitCode:
                    exitCode = r['exitCode']
                ret['desc'].append(r['desc'])
        ret['result'] = True
        ret['exitCode'] = exitCode
        ret['desc'] = "<->".join(ret['desc'])
        return ret  

    def _getRegister(self):
        try:
            import pg
        except Exception as e:
            log.warning("import module: {0}".format(e))
            return {"register_number": None}
        config = self._getConfig()
        accounts = config.get(self.gamename,'acctb')
        sql = "select count(*) from {0}".format(accounts)
        conn = pg.DB(host='db',dbname=self.dbname,user="postgres")
        accountNum = conn.query(sql).dictresult()[0]['count']
        return {"register_number": accountNum}

class wly(base):
    def __init__(self):
        self.dbname = "lyingdragon2"
        self.gamename = "lyingdragon"
        self.gamepath = self.gamename
        self.ip = "127.0.0.1"
        self.port = 5559

    def getAdminAddr(self,params):
        ret = {"result":True,"comment": {}}
        config = self._getConfig()
        jsonfile = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        if not params.has_key('key'):
            ret["result"] = False
            ret['commect'].update({"msg":"参数错误"})
        key = params.get('key')
        if not os.path.isfile(jsonfile):
            ret['result'] = False
            ret['comment'].update({"msg":"文件不存在"})
            return ret
        content = json.load(open(jsonfile,"r"),encoding="utf-8")
        for node in key.split('.'):
            content = content.get(node)
            if content is None:
                break
        ret['comment'].update({key:content})
        return ret

    def getKeyMap(self,params):
        keyDict = {
            "adminurl": "admin.url",
            "authip": "admin.auth.ip",
            "authuser" : "admin.auth.user",
            "servername": "server.name",
            "peername": "server.peer.name",
            "clusterid": "cluster.id",
            "paykey" : "ops.auth.pay",
            "domain": "server.report.address",
            "battleaddress" : "store.address"
            }
        if keyDict.has_key(params['key']):
            params['key'] = keyDict[params['key']]
            return params
        else:
            return {"result": False,"comment":{"msg":"不支持的方法"}}

    def setConfig(self,params):
        config = self._getConfig()
        ret = {"result":True,"comment": {}}
        if not params.has_key('key'):
            ret["result"] = False
            ret['commect'].update({"msg":"参数错误"})
        key = params.get('key')
        value = params.get("value")
        jsonfile = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        if not os.path.isfile(jsonfile):
            ret['result'] = False
            ret['comment'].update({"msg":"文件不存在"})
            return ret
        content = json.load(open(jsonfile,"r"),encoding="utf-8")
        if params.get("bak") is True:
            shutil.copy2(jsonfile,"{0}.{1}".format(jsonfile,int(time.time())))
        content = self._changeDict(content,key,value)
        with salt.utils.fopen(jsonfile,"w") as fp_:
            content = json.dumps(content,
                                 encoding="utf-8",
                                 ensure_ascii=False,
                                 indent=6,
                                 sort_keys=True)
            log.error(content)
            fp_.write(content)

            ret["comment"].update({"msg":"修改成功"})
        return ret

    def _changeDict(self,content,key,value):

        t = 'content'
        for i in key.split('.'):
            t += '["'+str(i)+'"]'
            if not content.has_key(i):
                exec(t + '={}')
        exec(t + '=value')
        return content

    def getCrossServer(self):
        ret = {"result":True,"comment": {}}
        config = self._getConfig()
        jsonfile = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        if not os.path.isfile(jsonfile):
            ret['result'] = False
            ret['comment'].update({"msg":"文件不存在"})
            return ret
        content = json.load(open(jsonfile,"r"),encoding="utf-8")
        if not content.has_key("cluster"):
            ret['result'] = False
            ret['comment'].update({"msg":"该服务器没有跨服配置"})
            return ret
        ret['comment'].update({"id":content['cluster']['id'].split(';')})
        return ret






    def getServerInfo(self,**kwargs):
        import urllib2
        ip = "127.0.0.1"
        port = 5559
        url = 'http://%s:5280/public/player_num' % ip
        try:
            result = json.loads(urllib2.urlopen(url).read())
        except Exception as e:
            result = {}
            log.error("open link:{0},{1}".format(url,e))
        data  = self.doSth(ip,port,"version\n")
        ret = {}
        if data['code'] == False:
            ret['server_version'] = None
        else:
            ret['server_version'] = data['desc'].split(" ")[0]
        if result.has_key("online_num"):
            ret['online_number'] = result['online_num']
            ret['register_number'] = result['registed']
        else:
            ret['online_number'] = None
            ret['register_number'] = None
        ret.update(self._getIP())
        ret['client_version'] = __grains__['webversion']
        ret['gamename'] = self.gamename
        ret['result'] = True
        return ret




class khbd(base):
    def __init__(self):
        self.dbname = "dreamback"
        self.gamename = self.dbname
        self.gamepath = self.dbname
        self.ip = "127.0.0.1"
        self.port = 8888

    def getServerInfo(self,*args,**kwargs):
        port = 8888
        host = "127.0.0.1"
        result = self.doSth(host,port,"ver\r\n")
        ret = {}
        ret.update(self._getRegister())
        ret.update({'ipaddr':__grains__['ipv4']})
        ret['gamename'] = self.gamename
        if result['code'] is False:
            ret['server_version'] = None
            ret['build_time'] = None
            log.warning("Get data faild")
        else:
            result = result['desc'].split(r'|')
            ret['server_version'] = result[0]
            ret['build_time'] = result[1]
        ret['result'] = True
        return ret

    def getKeyMap(self,params):
        keyDict = {
            "adminurl": "admin.url",
            "authip": "admin.auth.ip",
            "authuser" : "admin.auth.user",
            "servername": "server.name",
            "peername": "server.peer.name",
            "paykey" : "ops.auth.pay",
            "domain": "server.host",
            "clusterid" : "server.peer.cluster.id",
            "battleaddress" : "store.address"
            }
        if keyDict.has_key(params['key']):
            params['key'] = keyDict[params['key']]
            return params
        else:
            return {"result": False,"comment":{"msg":"不支持的方法"}}


class war(base):
    def __init__(self):
        self.dbname = "warcraft"
        self.gamename = self.dbname
        self.gamepath = self.dbname
        self.ip = "127.0.0.1"
        self.port = 5559
    def getServerinfo(self,*args,**kwargs):
        port = 5559
        ip = "127.0.0.1"
        ret = {}
        version = self.doSth(ip,port,"version\n")
        if version is False:
            ret['server_version'] = None
            ret['online_number'] = None
            log.error("Get server info failed!")
        else:
            ret['server_version'] = version
            online = self.doSth(ip,port,"state\n")
            online = [x for x in online.split(r":")]
            ret['online_number'] = online[1]
        log.info("{0}: {1}".format(version,online))
        ret.update(self._getRegister())
        ret.update(self._getIP())
        return ret
    def getKeyMap(self,params):
        keyDict = {
            "adminurl": "admin.url",
            "authip": "admin.auth.ip",
            "authuser" : "admin.auth.user",
            "servername": "server.name",
            "peername": "server.peer.name",
            "paykey" : "ops.auth.pay",
            "cluster": "cluster.id",
            "domain": "server.domain",
            "battleaddress" : "store.address"
            }
        if keyDict.has_key(params['key']):
            params['key'] = keyDict[params['key']]
            return params
        else:
            return {"result": False,"comment":{"msg":"不支持的方法"}}


class mhjh(base):
    def __init__(self):
        self.dbname = "legendary"
        self.gamename = self.dbname
        self.gamepath = self.dbname
    def _initUrllib(self):
        username = "uqeeadmin"
        password = 'soidc..123'
        port = 9131
        ip = self._getIpByPort(port)
        _url = "http://%s:%s/admin/server" %(ip,port)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()  #创建密码管理器
        password_mgr.add_password(None,_url,username,password)   #增加帐号密码到管理器
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)    #生成handler
        opener = urllib2.build_opener(handler)    #生成opener
        urllib2.install_opener(opener)    #安装opener
        return _url

    def getServerInfo(self,*args,**kwargs):
        _url = self._initUrllib()
        ret = {}
        try:
            result = urllib2.urlopen(_url)
            ret['online_number'] = result.read()
        except:
            ret['online_number'] = None
            log.error("Get server info failed")
        ret.update(self._getRegister())
        ret['gamename'] = self.gamename
        ret.update(self._getIP())
        ret['result'] = True
        return ret


    def getKeyMap(self,params):
        keyDict = {
            "adminurl": "admin.url",
            "authip": "admin.auth.ip",
            "authuser" : "admin.auth.user",
            "servername": "server.name",
            "peername": "server.peer.name",
            "paykey" : "ops.auth.pay",
            "domain": "server.report.address",
            "showname": "server.showname",
            "lang" : "server.language",
            "battleaddress" : "store.address"
            }
        if keyDict.has_key(params['key']):
            params['key'] = keyDict[params['key']]
            return params
        else:
            return {"result": False,"comment":{"msg":"不支持的方法"}}
    def rollBack(self,params,**kwargs):
        ret = {"result": True,"comment":{}}
        cmd = ['php']
        cmd.append(script)
        cmd.append('-m legendary')
        if kwargs.get("filename") and os.path.isfile(kwargs.get(filename)):
            cmd.append('-f {0}'.format(kwargs.get(filename)))
        else: #如果有指定备份文件退出
            ret["result"] = False
            ret['comment'].update({"msg":"back filename is not specify"})
            return ret
        what = list()
        if kwargs.get('item'):
            what.append('i')
        if kwargs.get('pet'):
            what.append('p')
        if kwargs.get('askkey'):
            what.append('a')
        if len(what) == 0:
            ret["result"] = False
            ret['comment'].update({"msg":"roll project is not specify"})
            return ret
        else:
            cmd.append("-w {0}".format("".join(what)))
        if kwargs.get('roleid'):
            cmd.append("-u {0}".kwargs.get('roleid'))
        else:
            ret["result"] = False
            ret['comment'].update({"msg":"roleid is not specify"})
            return ret

        runningGame = __salt__['uqee_chkgame.checkgame']()
        if runningGame:
            ret["result"] = False
            ret['comment'].update({"msg":runningGame})
            return ret  #如果有游戏已经在运行. 返回检查结果
        script = "/tmp/roleRollBack.php"
        source = "salt://conf/rollback_user.php"
        if not __salt__['cp.get_file'](source,script,makedirs=True):
            ret["result"] = False
            ret['comment'].update({"msg":"update script failed"})
            return ret




class mycs(base):
    def __init__(self):
        self.dbname = "naruto"
        self.gamename = self.dbname
        self.gamepath = self.dbname
        self.ip = None
        self.port = 9132

    def getServerInfo(self,*args,**kwargs):
        ip = self._getIpByPort(9132)
        url = 'http://%s:9132/admin/online' % ip
        ret = {}
        ret.update(self._getRegister())
        ret['gamename'] = self.gamename
        try :
            result = urllib2.urlopen(url).read()
            ret['online_number'] = result
        except:
            ret['online_number'] = None
            log.error("open link:{0} faild".format(url))
        ip = self._getIpByPort(9130)
        url = 'http://%s:9130/serverinfo' %ip
        try:
            result = eval(urllib2.urlopen(url).read())
            ret['server_version'] = result['version']
            res['build_time'] = result['build_date']
        except:
            ret['server_version'] = None
            ret['build_time'] = None
            log.error("open link:{0} faild".format(url))
        ret.update(self._getIP())
        ret['result'] = True
        return ret


    def getKeyMap(self,params):
        keyDict = {
            "adminurl": "admin.url",
            "authip": "admin.auth.ip",
            "authuser" : "admin.auth.user",
            "servername": "server.name",
            "peername": "server.peer.name",
            "paykey" : "ops.auth.pay",
            "domain": "server.report.address",
            "battleaddress" : "store.address",
            "clusterid" : "cluster.id"
            }
        if keyDict.has_key(params['key']):
            params['key'] = keyDict[params['key']]
            return params
        else:
            return {"result": False,"comment":{"msg":"不支持的方法"}}



class nwzr(base):
    '''
    女巫之刃相关操作
    关游戏开游戏 都继承卧龙吟的方法
    '''
    def __init__(self):
        self.dbname = "nwzr"
        self.gamename = "q5"
        self.gamepath = self.dbname
        self.ip = "127.0.0.1"
        self.port = 5559

    def getServerInfo(self):
        ret = {"gamename":self.gamename,'result':True}
        ip = self._getIpByPort(5280)
        if not ip:
            return ret
        url = "http://{0}:5280/serverinfo".format(ip)
        try:
            result = eval(urllib2.urlopen(url).read().strip())
            ret['online_number'] = result['online_num']
            ret['server_number'] = result['version']
            ret['register_number'] = result['account_num']
            ret['build_time'] = result['build_date']
            ret['server_time'] = result['now']
            ret['gamename'] = self.gamename
        except:
            log.error("open link:{0} faild".format(url))
            ret['result'] = False
            ret['error'] = "游戏未开启或访问接口失败"
            return ret
        return ret
    def getKeyMap(self,params):
        keyDict = {
            "adminurl": "admin.url",
            "authip": "admin.auth.ip",
            "authuser" : "admin.auth.user",
            "servername": "server.name",
            "peername": "server.peer.name",
            "paykey" : "ops.auth.pay",
            "domain": "server.report.address",
            "battleaddress" : "store.address",
            }
        if keyDict.has_key(params['key']):
            params['key'] = keyDict[params['key']]
            return params
        else:
            return {"result": False,"comment":{"msg":"不支持的方法"}}


class rh(base):
    def __init__(self):
        self.dbname = "card"
        self.port = 9210
        self.ip = '127.0.0.1'
        self.gamename = 'card'
        self.gamepath = self.gamename

    def getServerInfo(self):
        ret = {}
        result = self.doSth(self.ip,self.port,'status\n')
        if result['code'] is False:
            ret['server_version'] = None
            ret['register_number'] = None
            ret['online_number'] = None
        else:
            result = json.loads(result['desc'])
            ret['server_version'] = result['version']
            ret['register_number'] = result['createNums']
            ret['online_number'] = result['onlineNums']
        ret.update(self._getIP())
        return ret


class djwy(base):
    def __init__(self):
        self.dbname = 'pswordsman'
        self.port = 9118
        self.ip = '127.0.0.1'
        self.gamename = 'pswordsman'
        self.gamepath = self.gamename

    def copyGame(self,params):
        ret = {
            "result": False,
            "comment" : ""
        }
        is_remote = False
        if __grains__.get('game_server_type',1) == 1:
            ret['comment'] = '游戏服务器不是单服多区'
            return ret
        if not params.has_key('src'):
            ret['comment'] = '源文件不能空'
            return ret
        if params['src'].find(':') != -1:
            is_remote = True
        if not params.has_key('dest'):
            ret['comment'] = '目标文件不能空'
            return ret;
        if not params.has_key('server_id'):
            ret['comment'] = '服务器ID不能空'
            return ret
        server_list = __grains__.get('server_list',[]);
        if len(server_list) == 0:
            ret['comment'] = '请先配置区服'
            return ret
        server = dict();
        for item in server_list:
            if item.get('server_id') == params['server_id']:
                index = server_list.index(item)
                server = item
                break;
        else:
            ret['comment'] = '该服务器ID,不在已配置的区服中'
            return ret
        if __salt__['postgres.db_exists'](server['dbname'],host='db',user='postgres',port=5432):
            ret['comment'] = '数据库已存在'
            return ret
        else:
            __salt__['postgres.db_create'](server['dbname'],host='db',user='postgres',port=5432)
        if os.path.isdir(params['dest']) or \
        os.path.isfile(params['dest']):
            ret['comment'] = '目标文件已存在'
            return ret

        if is_remote:
            prev,src = params['src'].split(':')
            __salt__['grains.setval']('prev',prev);
            r = __salt__['uqee_scp.copyfile'](src,params['dest'])
        else:
            try:
                shutil.copytree(params['src'],params['dest'],True)
                r = True
            except Exception as e:
                r = False
                pass

        if r is not True:
            ret['comment'] = '复制文件失败'
            return ret
        dest = '';
        if os.path.isfile(params['dest']):
            dest = os.path.dirname(params['dest'])
        else:
            dest = params['dest']
        server['work_dir'] = dest
        dest = os.path.join(dest,self.gamename,'config.json')
        json_conent = self.__getGameConfigDict(dest);
        if json_conent is False:
            ret['comment'] = '游戏配置文件不存在或文件格式错误'
            return ret
        json_conent['server']['id'] = server['server_id'];
        json_conent['server']['name'] = server['server_name'];
        json_conent['server']['sock']['port'] = server['sock_port']
        json_conent['server']['sock']['admin']['port'] = server['console_port']
        json_conent['server']['http']['admin']['port'] = server['admin_port']
        json_conent['server']['http']['ops']['port'] = server['ops_port']
        json_conent['db'] = {"connection":{"string": "dbname={0} user=postgres host=db".format(server['dbname'])}}
        json_conent['server']['host'] = server['domain']
        server_list[index] = server;
        __salt__['grains.setval']('server_list',server_list)
        with open(dest,'w') as _fp:
            _fp.write(json.dumps(json_conent,False,False,indent=4))
        ret['comment'] = '复制区服成功,自行导入数据库结构表'
        ret['server'] = server
        ret['result'] = True
        return ret


    def setCopyConfig(self,params):
        ret = {
            "result": False,
            "comment" : ""
        }
        if __grains__.get('game_server_type',1) == 1:
            ret['comment'] = '游戏服务器不是单服多区'
            return ret
        sock_port = 22000
        admin_port = 20000
        ops_port = 21000
        console_port = 5500;
        server_list = __grains__.get('server_list',[]);
        server = dict();
        if 'server_name' not in params.keys():
            ret['comment'] = '服务器名称不能空';
            return ret;
        server['server_name'] = params['server_name'];
        if 'server_id' not in params.keys():
            ret['comment'] = '服务器ID不能空';
            return ret;
        server['server_id'] = params['server_id']
        if 'dbname' not in params.keys():
            ret['comment'] = '数据库名称不能空'
            return ret
        if __salt__['postgres.db_exists'](params['dbname'],host='db',user='postgres',port=5432):
            ret['comment'] = '数据库已存在'
            return ret;
        server['dbname'] = params['dbname']
        if params.get('domain') is None:
            ret['comment'] = '游戏域名不能为空'
            return ret
        domain = params.get('domain')
        if isinstance(server_list,types.ListType) :
            for item in server_list:
                if server['dbname'] == item['dbname'] or \
                server['server_id'] ==  item['server_id'] or \
                server['server_name'] == item['server_name'] or\
                item['domain'] == domain:
                    ret['comment'] = '配置与已有服冲突';
                    ret['server_list'] = server_list
                    return ret;
                sock_port = item['sock_port'] if item['sock_port'] > sock_port else sock_port
                admin_port = item['admin_port'] if item['admin_port'] > admin_port else admin_port
                ops_port = item['ops_port'] if item['ops_port'] > ops_port else ops_port
                console_port = item['console_port'] if item['console_port'] > console_port else console_port
        server['admin_port'] = admin_port + 1;
        server['ops_port'] = ops_port +1 
        server['sock_port'] = sock_port + 1
        server['console_port'] = console_port + 1
        server['domain'] = domain
        server['is_notify'] = False
        if len(server_list) == 0:
            __salt__['grains.setval']('server_list',list());
        __salt__['grains.append']('server_list',server);
        # ret['server_list'] = __grains__['server_list']
        ret['result'] = True;
        ret['comment'] = '设置成功';
        return ret


    def monitor(self,*args,**kwargs): 
        ret = {
            "result": False,
            "desc" : "",
            "exitCode" : 0,
        }
        game_server_type = __grains__.get('game_server_type',1)
        if game_server_type == 1:
            ret['desc'] = 'game_server_type error'
            return ret
        server_list = __grains__.get('server_list',[])
        if len(server_list) == 0:
            ret['desc'] = 'please config server_list'
            return ret
        config = self._getConfig()
        if not config.has_section(self.gamename) or \
        not config.has_option(self.gamename,'process'):
            ret['desc'] = 'not found section in gameinfo.conf'
            return ret
        checkList = config.get(self.gamename,'process');
        try:
            checkList = eval(checkList)
        except Exception as e:
            log.error('eval process fail'+str(e))
            ret['desc'] = 'process error in gameinfo.conf'
            return ret
        clist = []
        for item in checkList:
            for server in server_list:
                if server.get('is_notify') is False:
                    continue
                c = item.copy();
                c['port'] = server['sock_port']
                c['name'] = "{0}:{1}".format(server['server_name'],item['name'])
                clist.append(c)
        r = self.monitorBase(check_list=clist)
        if r['exitCode'] == 2:
           start_res = self.startgame(start_all=True)
           r['desc'] = '{0}, {1}'.format(r['desc'],'restart now!')
        ret['result'] = r['result'];
        ret['desc'] = r['desc'];
        ret['exitCode'] = r['exitCode']
        return ret

    def __getGameConfigDict(self,dest=None):
        if dest is None or not os.path.isfile(dest):
            dest = os.path.dirname(__file__) + "/djwy/config.json"
        with open(dest,"rb") as fp:
            try:
                content = json.loads(fp.read(),'utf-8');
            except Exception as e:
                log.error('游戏配置文件不存在或文件格式错误'+e.message)
                return False
            if isinstance(content,types.DictType):
                return content;
            else:
                return False


class koudai(base):
    def __init__(self):
        self.dbname = "naughty"
        self.port = 9000
        self.ip = '127.0.0.1'
        self.gamename = 'naughty'
        self.gamepath = 'naughty'

    def getServerInfo(self,*args,**kwargs):
        ret = {"code": True,"desc": "OK"}
        ret.update(self._getRegister());
        return ret
class pzero(base):
    def __init__(self):
        self.dbname = "pzero"
        self.port = 9118
        self.ip = '127.0.0.1'
        self.gamename = 'pzero'
        self.gamepath = 'pzero'

    def getServerInfo(self,*args,**kwargs):
        ret = {"code": False,"desc": "OK"}
        
        return ret

class sanguo(base):
    def __init__(self):
        self.dbname = "tapsanguo"
        self.port = 9118
        self.ip = '127.0.0.1'
        self.gamename = 'tap_sanguo'
        self.gamepath = 'sanguo'


class khbd_h5(base):
    def __init__(self):
        self.dbname = "khbd_h5"
        self.port = 9118
        self.ip = '127.0.0.1'
        self.gamename = 'khbd_h5'
        self.gamepath = 'khbd_h5'


class t3g_h5(base):
    def __init__(self):
        self.dbname = 't3g_h5'
        self.port = 9000
        self.ip = '127.0.0.1'
        self.gamename = self.dbname
        self.gamepath = self.dbname



class mengxin(base):
    def __init__(self):
        self.dbname = "mengxin"
        self.port = 9118
        self.ip = '127.0.0.1'
        self.gamename = self.dbname
        self.gamepath = self.dbname


    def getServerInfo(self, *args, **kwargs):
        ret = {}
	ret.update({'ipaddr':__grains__['ipv4']})
	ret.update(self._getRegister())
        config = self._getConfig()
        jsonfile = "/etc/conf/uqee/{0}/server/config.json".format(self.gamepath)
        if not os.path.isfile(jsonfile):
		pass
        content = json.load(open(jsonfile,"r"),encoding="utf-8")
        if not content.has_key("server"):
		pass
        ret['server_id'] = content['server']['id']
	ret['gamename'] = self.gamename
	ret['result'] = True
        return ret


class mysocket(object):
    def __init__(self,filename,destfilename):
        self.filename = filename
        self.destfilename = destfilename
        ip = 'databak.domain.com'
        port = 60000
        self.logger = log
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((ip,port))
            self.logger.info('{0}:{1}连接成功!'.format(ip,port))
        except Exception,e:
            self.logger.error("{0}:{1}连接失败,{2}!\n退出".format(ip,port,e))
            sys.exit(1)
        if self.confirm():
            self.sendfile()
    def recvfile(self):
        self.logger.info("server ready, now client rece file~~")
        f = open(self.filename, 'wb')
        while True:
            data = self.s.recv(4096)
            if data == 'EOF':
                print "recv file success!"
                break
            f.write(data)
        f.close()
    def sendfile(self):
        self.logger.info("server ready, now client sending file~~")
        f = open(self.filename, 'rb')
        while True:
            data = f.read(4096)
            if not data:
                break
            self.s.sendall(data)
        f.close()
        time.sleep(1)
        self.s.sendall('EOF')
        self.logger.info("send file success!")

    def confirm(self):
        client_command = "put %s %s" %(self.filename,self.destfilename)
        self.s.send(client_command)
        data = self.s.recv(4096)
        if data == 'ready':
            return True

    def __del__(self):
        self.s.close();
        __salt__['file.remove'](self.filename)
        self.logger.info('上传完毕,断开连接!')

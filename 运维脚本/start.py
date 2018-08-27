#!/usr/bin/env python
#encoding=utf-8
import salt.client
import salt.config
import salt.loader
import os,sys,time,logging
from optparse import OptionParser

echo = sys.stdout.write
end = sys.stdout.flush

def error(msg):
    nstr = "\033[31m{0}\033[0m".format(msg)
    print nstr
    exit(2)
def notify(msg,cl=32):
    return "\033[{0}m{1}\033[0m".format(cl,msg)
def start(sid,func,argc,kwarg=None,timeout=360,expr_form="glob"):
    btime = int(time.time())
    echo(notify("Log.info:------正在执行函数:{0},参数:{1},请稍等…… !\t"\
                     .format(func,argc),36))
    end()
    ret = localClient.cmd(sid,func,argc,timeout,expr_form,kwarg=kwarg)
    echo(notify("用时间{0}秒 !\n"\
                     .format(int(time.time()) - btime),35))
    if ret.values().__len__() == 0:
        error("客户端 {0}:{1}:{2} 没有正常返回!".format(sid,func," ".join(argc)))
    return ret
def init(sid):
    print notify('正在同步静态文件')
    start(sid,'saltutil.sync_all',[])
    start(sid,'saltutil.refresh_pillar',[])
    start(sid,setval,['sqllist',None,True])
    # ret = start(sid,'uqee_chkgame.checkgame',[])
    # if ret[sid] is not False:
    #     error(ret[sid])
def getInstallState(sid,key):
    ret = start(sid,'grains.get',[key],timeout=10)
    if ret.get(sid):
        return ret[sid]
    else:
        return False

def logger():
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S %A',
                filename='/var/log/start_config_game.log',
                filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    #logging.getLogger('').addHandler(console)
    return logging


def getgid(ip):
    ret = start(ip,'grains.items',[],timeout=10,expr_form='ipcidr')
    #print ret
    if ret.values().__len__() == 1:
        localhost = ret.values()[0]['localhost']
        # if localhost.split('-').__len__() != 3:
        #     print error("服务器Hostname错误:{0}".format(localhost))
        return ret.values()[0]['id']
    else:
        return False
def checkParams():
    if args.__len__() < 1:
        error('缺少ID或游戏安装包的名称')
    return getgid(args[0])
def parseResult(ret,sid):
    r = True
    if sid not in ret.keys():
        error("{0} 请求服务器超时!".format(sid))
    try:
        #notify_method = raw_input if option.notify is None else print
        for key,value in ret[sid].items():
            if value['result'] != True:
                r = False
                msg = notify('''修改系统参数或安装服务失败,
失败名称:{0}
具体原因:{1}
安装完成后请检查,回车继续!'''.format(key,value))
                if option.notify is False:
                    print msg
                else:
                    raw_input(msg)
        return r
    except:
        print ret[sid]
def copyFile(sid):
    '设置安装完成后复制哪个区的文件'
    if option.alias == None:
        qufu = raw_input(notify('请输入要复制文件的区服名(名称一定要和堡垒机hosts里面的名字相同):'))
    else:
        qufu = option.alias
    logger.info("输入区服名称: {0}".format(qufu))
    opts = salt.config.master_config('/etc/salt/master')
    opts['grains'] = salt.loader.grains(opts)
    mods = salt.loader.minion_mods(opts)
    prev = mods['hosts.get_ip'](qufu)
    if option.version == None:
        version = raw_input(notify('请输入服务端版本,例. v1.3.2 : '))
    else:
        version = option.version
    logger.info("当前输入版本: {0}".format(version))
    start(sid,setval,['server_version',version])
    if prev is not '':
        start(sid,setval,['prev',prev])
    else:
        start(sid,setval,['prev',False])
        raw_input(notify('输入的区服不存在,安装完成后请手动复制文件,或Ctrl+C退出脚本并重新运行.'))

def main(sid):
    init(sid)
    #start(sid,'cmd.run',['invoke-rc.d salt-minion restart'])
    print notify("salt测试版本,本脚本将清除以下数据库重新创建,请大家注意!")
    if option.notify == True:
        input(notify('gamedb game_log battle_report,如无疑问任意键继续,否则Ctrl+C退出:'))
    if option.game_server_type is None:
        game_server_type = raw_input(notify('是否为一服多区,1:否,2:是 :'))
        if len(game_server_type) == 0:
            error("请选择")
        game_server_type = int(game_server_type)
    else:
        game_server_type = int(option.game_server_type)
    if game_server_type not in [1,2]:
        error('game_server_type错误')
    server_list = start(sid,'grains.get',['server_list',[]])
    if len(server_list.get(sid)) == 0:
        if option.hostname == None:
            hostname =  raw_input(notify("请输入主机名称: "))
        else:
            hostname = option.hostname
        if option.ssl == None:
            ssl = raw_input(notify('是否启用SSL,注意,目前只支持EFUNFUN平台:1.启用,0.不启用(默认):'))
            if ssl != '1':
                ssl = 0
        else:
            ssl = option.ssl
        logger.info("SSL配置选择结果: {0}".format(ssl))
        if option.log == None:
            player_state = raw_input(notify('是否启用日志中心,1.是(默认),0.不是(注意:这里选择错误会影响流失统计和日志记录.): '))
            if player_state != '0':
                player_state = 1
        else:
            player_state = option.log
        logger.info("是否启用日志中心: {0}".format(player_state))
        if option.preask == None:
            if raw_input(notify('是否启用preask,0:启用,1:不启用,默认启用,请输入: ')) != '1':
                preask = True
            else:
                preask = False
        else:
            preask = option.preask
        # if preask and option.wall_ip is None:
        #     wall_ip = raw_input(notify('墙IP,请输入: '))
        # elif preask and option.wall_ip:
        #     wall_ip = option.wall_ip
        # else:
        #     wall_ip = False
        logger.info("是否启用preask: {0}".format(preask))
        copyFile(sid)
        start(sid,'uqee_chkgame.hostname',[hostname])
        start(sid,'grains.setval',['localhost',hostname])
        # start(sid,'grains.setval',['wall_ip',wall_ip])
        gname = start(sid,'pillar.get',['game:gamename'])[sid]
        start(sid,setval,['gamename',gname])
        start(sid,setval,['ssl',ssl])
        start(sid,setval,['player_state',player_state])
        start(sid,setval,['preask',preask])
    if game_server_type == 2:
        server_name = raw_input(notify('请输入服务器名称 :'))
        if len(server_name) == 0:
            error('请输入服务器名称')
        logger.info('输入的服务器名称:'+server_name)
        dbname = raw_input(notify('请输入数据库名称 :'))
        if len(dbname) == 0:
            error('请输入数据库名称');
        logger.info('输入的数据库名称是:' + dbname)
        server_id = raw_input(notify('请输入服务器ID :'))
        if len(server_id) == 0:
            error('请输入服务器ID')
        logger.info("输入的数据库名称是: "+server_id)
        src = raw_input(notify("请输入要复制的区服目录\n支持远程服务器,如:10.0.0.1:/root/workspace/gamename :"))
        if len(src) == 0:
            error("请输入源地址")
        logger.info("源地址是 :"+src)
        dest = raw_input(notify("请输入目标地址(绝对路径) :"))
        if len(dest) == 0:
            error('请输入目录地址')
        logger.info("目标地址是:" + dest)
        domain = raw_input(notify('请输入服务器域名: '))
        if len(domain) == 0:
            error('请输入域名')
        logger.info('域名: '+domain)
        start(sid,setval,['game_server_type',game_server_type])
    # 如果是第一个服的时候就安装所有系统配置及游戏配置
    # 否则什么都安装
    start(sid,setval,['gamepackage','game-init'])
    print notify('静态文件同步完毕,正在设置区服参数!')
    actions = ['system','pam','game.postgresql','game.cron','game.web','game.report','game.game',
               'game.player_state','nagios','game.zabbix','game.after','system.updategrains']
    if game_server_type == 1 and gname == 'card': #如果游戏是奔跑,就安装mongodb
        actions.insert(actions.index('game.game'),'game.mongodb')
    
    if game_server_type == 2 and len(server_list) > 0:
        actions = []

    for action in actions:
        #如果已经安装过系统环境就不在安装
        # if action == 'system' and getInstallState(sid,'install_system'):
        #     action = 'system.iptable'
        #如果已经安装过ldap ssh认证. 就不在安装
        #if action == 'pam' and getInstallState(sid,'install_pam'):continue
        ret = start(sid,state,[action],{},1200)
        if parseResult(ret,sid):
            if action == 'pam':
                #如果pam安装成功.就设置一个grains值表名之服务器. 已经成功安装pam
                start(sid,setval,['install_pam',True])
    if game_server_type == 2:
        params = {
            "server_name":server_name,
            "server_id" : server_id,
            "dbname": dbname,
            "domain" : domain,
        }
        ret = start(sid,'uqee.set_copy',[],kwarg=params)
        if ret.get(sid,{}).get('result',False) is not True:
            error(ret.get(sid).get('comment'))
        params = {
            "server_id" : server_id,
            "src" : src,
            "dest" : dest,
            }
        ret = start(sid,'uqee.copy_game',[],kwarg=params)
        if ret.get(sid,{}).get('result',False) is not True:
            error(ret.get(sid).get('comment'))
        print notify(ret.get(sid).get('comment'))
    start(sid,setval,['is_notify',False])  #装好游戏后默认是关闭手机报警的.
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-s","--ssl",dest="ssl",
                      help="是否启用ssl,启用:1,不启用:0".decode("utf-8")
                      )
    parser.add_option("-t","--game_server_type",dest="game_server_type",
                      help="设置为一服多区服务器".decode("utf-8")
                      )
    parser.add_option("-l","--log",dest="log",
                      help="是否启用日志中心,启用:1,不启用:0".decode("utf-8")
                      )
    parser.add_option("-v","--version",dest="version",
                      help="指定数据库版本,如: v2.2.0".decode("utf-8"))
    parser.add_option("-a","--alias",dest="alias",
                      help="要复制文件的区服名(名称一定要和堡垒机hosts里面的名字相同".decode("utf-8"))
    parser.add_option("-p","--preask",dest="preask",
                      help="是否启用preask,启用:1,不启:0".decode("utf-8"),
                      )
    parser.add_option("-H","--hostname",dest="hostname",
                      help="指定服务器主机名".decode("utf-8"),
                      )
    parser.add_option("-n","--notify",dest="notify",
                      help="不显示提示信息".decode("utf-8"),action="store_false")
    # parser.add_option("-w",'--wall_ip',dest='wall_ip',
    #                   help="specify a ip of wall")
    (option,args) = parser.parse_args()

    startTime = int(time.time())
    logger = logger()
    print notify("------------------------开始安装环境------------------------")
    print notify('正在初始化,请稍等…………')
    localClient = salt.client.LocalClient()
    state = 'state.sls'
    setval = 'grains.setval'

    sid = checkParams()
    if sid is False:
        ret = int(time.time()) - startTime
        error('该服务器没有找到,请检查salt是否安装正确,如果正常请稍后再试')
    main(sid)
    print notify('请检查战报地址是不是正常',31)
    print notify('安装游戏成功,用时%d秒,请检查!' % (int(time.time()) - startTime,),33)



#1111
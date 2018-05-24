#!/usr/bin/env python
#encoding=utf-8
#
import salt.loader,salt.config,salt.output
from optparse import OptionParser
def parseArgs():
    optparse = OptionParser()
    optparse.add_option("-a","--shut-all",action="store_true",help="关闭所有区服".decode("utf-8"))
    optparse.add_option('-s','--server-id',dest="server_id",help="指定关闭区服的ID,有-a参数时此参数无效".decode("utf-8"))
    optparse.add_option('-u','--username',dest="username",help="配置文件中的帐号".decode("utf-8"))
    optparse.add_option('-p','--password',dest="password",help="配置文件中的密码".decode("utf-8"))
    return optparse.parse_args()
def notify(msg,cl=32):
    '''
    @param msg string 要输出的信息
    @param cl int 要输出信息的颜色,见linux的颜色列表
    @return 返回要输出的字符串
    '''
    nstr = "\033[{0}m{1}\033[0m".format(cl,msg)
    return nstr
def get_server_id(server_list):
    if server_list is None:
        return None
    msg = "请选择你要关闭的区服:\n";
    for item in server_list:
        index = server_list.index(item)
        msg += "{0} => {1}\n".format(index,item.get('server_name',None))
    msg += "请输入: "
    item_id = raw_input(notify(msg))
    if not item_id.isdigit():
        print notify('输入错误',31)
        exit(0)
    item_id = int(item_id)
    return server_list[item_id].get('server_id')

def main():
    options,args = parseArgs()
    opts = salt.config.minion_config('/etc/salt/minion')
    opts['grains'] = salt.loader.grains(opts)
    opts.update(salt.minion.resolve_dns(opts))
    minion = salt.loader.minion_mods(opts)
    if not minion.has_key('uqee.sync_all'):
        minion['saltutil.sync_all']()
    game_server_type = opts['grains'].get('game_server_type',1)
    server_id = options.server_id
    if options.shut_all is None and options.server_id is None:
        server_id = get_server_id(opts['grains'].get('server_list',None))
    params = {
        "shut_all" : options.shut_all,
        "server_id": server_id
    }
    if options.username:
        params['username'] = options.username
    if options.password:
        params['password'] = options.password
    ret = minion['uqee.shut_game'](**params)
    salt.output.display_output(ret,'nested',opts)
    exit(0)


if __name__ == '__main__':
    main()

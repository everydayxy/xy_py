#!/usr/bin/env python
#coding:utf-8
#开服自动配置服务端json文件
#自动配置葵花客户端xml文件，不适用khyqios,kh91sj,khhutong 域名格式不同 开的也很少
import json
import sys
import os
import xml.etree.ElementTree as et
import salt.config
import salt.loader
from shutil import copyfile

reload(sys)
sys.setdefaultencoding('utf8')

def getgrains():
    minion_conf=salt.config.client_config('/etc/salt/minon')
    grains=salt.loader.grains(minion_conf)
    gamename = grains['gamename']
    ip = grains['ipv4'][1]
    hostname = grains['localhost'].split('-')
    sid = hostname[-1]
    return gamename,ip,sid

def rename_xml(oldsid,sid):
    xmlfile = '/home/soidc/wly_web/config/Servers{}.dat'.format(oldsid.lstrip('0'))
    new_xmlfile = '/home/soidc/wly_web/config/Servers{}.dat'.format(sid.lstrip('0'))
    #print xmlfile,new_xmlfile
    os.rename(xmlfile,new_xmlfile)
    return new_xmlfile

def change_conf():
    gamename,ip,sid = getgrains()
    copyfile('/etc/conf/uqee/{}/server/config.json'.format(gamename),'/etc/conf/uqee/{}/server/config.json.bak'.format(gamename))
    configfile = '/etc/conf/uqee/{}/server/config.json'.format(gamename)
    #configfile = '/etc/conf/uqee/{}/server/config.json.bak'.format(gamename)
    with open(configfile, 'r') as f:
        data = json.loads(f.read())
    if gamename == 'lyingdragon':
        ipauth = ['60.12.156.155','122.226.109.155','122.226.109.136','192.168.12.4','192.168.12.5','192.168.12.7','192.168.12.8','192.168.12.23','192.168.12.24']
        ipauth.insert(0, ip)
    else:
        ipauth = ['192.168.15.110','192.168.15.111','192.168.12.7','192.168.12.8','192.168.12.23','192.168.12.24']
        ipauth.insert(0,ip)
    newipauth = ';'.join(ipauth)
    oldid = data["server"]['id']
    id_value = oldid.split('-')
    id_value[-1] = sid
    newid = '-'.join(id_value)
    newname = sid.lstrip('0')+"区"
    if gamename == 'naughty' or gamename == 'khbd_h5':
            data['server']['id'] = newid
            data['peer']['local']['address'] = '{}:1268'.format(ip)
            data["server"]['name'] = newname
    elif gamename == 'mengxin':
            data["server"]['id'] = newid
    elif gamename == 'dreamback':
        copyfile('/home/soidc/khbd_web/config/Server.xml','/home/soidc/khbd_web/config/Server.xml.bak')
        xmlfile = '/home/soidc/khbd_web/config/Server.xml'
        oldservername=data['server']['name'].split('-')
        newservername ='{}-{}区'.format(oldservername[0],sid)
        olddomain = data['server']['host'].split('.')
        platform=olddomain[2]
        olddomain[0] = 's{}'.format(sid.lstrip('0'))
        newdomain = '.'.join(olddomain)
        khbd_xml(xmlfile,sid,newdomain,platform)
        data['admin']['auth']['ip'] = newipauth
        data['server']['host'] = newdomain
        data['server']['battle']['address'] = newdomain
        data['server']['id'] = newid
        data['server']['name'] = newservername
        data['server']["partner"]['id'] = sid
        data['server']['peer']["cluster"]["id"] = newid
        data['server']["peer"]["name"] = newname
        data['server']["web"]["admin"]["ip"] = ip
        try:
	    data['peer']['local']['address'] = '{}:1268'.format(ip)
        except Exception ,e:
	    print('error' ,e,'happened')
    elif gamename == 'legendary' or gamename == 'naruto':
        olddomain = data['server']['report']['address'].split('.')
        platform=olddomain[2]
        olddomain[0] = 's{}'.format(sid.lstrip('0'))
        newdomain = '.'.join(olddomain)
        data['admin']['auth']['ip'] = newipauth
        data['cluster']['id'] = newid
        data['server']['id'] = newid
        data['server']["partner"]['id'] = sid.lstrip('0')
        data['server']["report"]["address"] = newdomain
        if platform == 'aiwan':
            data['server']['name'] = "爱玩-{}区".format(sid)
            data['server']["showname"] = 's{}'.format(sid.lstrip('0'))
            data['server']["peer"]["name"] = newname
            data['server']['global'] = {
            "address": "{}:9110".format(ip),
            "admin": {
                "address": "{}:9111".format(ip),
                "eth": "eth1",
                "port":9111
            },
            "eth": "eth1",
            "port": "9110",
            "tunnel": {
                "address": "{}:9112".format(ip),
                "eth": "eth1",
                "port": 9112
            }
            }
        elif platform == 'lequ':
            data['server']['name'] = "乐趣-{}区".format(sid)
            if gamename == 'legendary':
                data['server']["peer"]["name"] = newname
                data['server']["showname"] = '<乐趣>s{}'.format(sid.lstrip('0'))
            elif gamename == 'naruto':
                data['server']["peer"]["name"] = '乐趣{}'.format(newname)
#                open_date = raw_input("Please input the game open date:")
#                data['server']["open"]["date"] = open_date
        elif platform == '2686':
            data['server']['name'] = '2686-{}区'.format(sid.lstrip('0'))
            data['server']["peer"]["name"] = '{}区'.format(sid.lstrip('0'))
            data['server']["showname"] = '<2686>h{}'.format(sid.lstrip('0'))
        elif platform == '1k2k' and gamename == 'naruto':
            data['server']['name'] = '1k2k-{}区'.format(sid.lstrip('0'))
            data['server']["peer"]["name"] = '1k2k-{}区'.format(sid.lstrip('0'))
    elif gamename == 'lyingdragon':
        platform = oldid.split('-')[-2]
        data['admin']['auth']['ip'] = newipauth
        data['cluster']['id'] = newid
        data['server']['id'] = newid
        data['server']['partner']['id'] = sid.lstrip('0')
        data['server']['peer']['name'] = newname
        data['peer']['local']['address'] = '{}:1268'.format(ip)
        if platform == 'lqw':
            data['server']['name'] = '乐趣{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.snsfun.com'.format(sid.lstrip('0'))
        elif platform == '1k2k':
            data['server']['name'] = '1k2k-{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.1k2k.com'.format(sid.lstrip('0'))
        elif platform == '2686':
            data['server']['name'] = '2686-{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.2686.com'.format(sid.lstrip('0'))
        elif platform == '5qwan':
            data['server']['name'] = '5qwan-{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.5qwan.com'.format(sid.lstrip('0'))
        elif platform == 'qq990':
            data['server']['name'] = 'QQ990-{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.qq990.com'.format(sid.lstrip('0'))
        elif platform == '789hi':
            data['server']['name'] = '789hi-{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.789hi.com'.format(sid.lstrip('0'))
        elif platform == 'lehh':
#data['peer']['center']['address'] = '{}:1268'.format(ip)
            data['server']['name'] = '乐嗨嗨{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.lehaihai.uqeegame.com'.format(sid.lstrip('0'))
#            data['server']['copainee'] = {
#              "address": "{}:3559".format(ip),
#              "id": "{}".format(newid),
#              "reportaddress": "s{}.wly.lehaihai.uqeegame.com".format(sid.lstrip('0'))
#          }
#           data['server']['followee'] = {
#              "address": "{}:3559".format(ip),
#              "id": "{}".format(newid),
#              "reportaddress": "s{}.wly.lehaihai.uqeegame.com".format(sid.lstrip('0'))
#          }
        elif platform == 'xiongmw':
            data['peer']['center']['address'] = '{}:1268'.format(ip)
            data['server']['name'] = '熊猫玩{}区'.format(sid.lstrip('0'))
            data['server']['report']['address'] = 's{}.wly.xiongmaowan.uqeegame.com'.format(sid.lstrip('0'))
            data['server']['copainee'] = {
              "address": "{}:3559".format(ip),
              "id": "{}".format(newid),
              "reportaddress": "s{}.wly.xiongmaowan.uqeegame.com".format(sid.lstrip('0'))
             }
            data['server']['followee'] = {
              "address": "{}:3559".format(ip),
              "id": "{}".format(newid),
              "reportaddress": "s{}.wly.xiongmaowan.uqeegame.com".format(sid.lstrip('0'))
            }
        oldconfigfile = '/etc/conf/uqee/lyingdragon/server/config.json.bak'
        with open(oldconfigfile) as f2:
            data2 = json.loads(f2.read())
            oldsid = data2['server']['partner']['id']
        new_xmlfile = rename_xml(oldsid, sid )
        wly_xml(new_xmlfile,sid,platform)

    with open(configfile, 'w') as f1:
        f1.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
        f1.write('\n')

def wly_xml(xmlfile,sid,platform):   #wly && khbd
    tree = et.parse(xmlfile)
    #newtitle = raw_input("请输入新的title:")
    for i in tree.iter(tag="ServerList"):
        i.attrib['ident'] = '{}'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8")
    for i in tree.iter(tag="Server"):
        if platform == 'lehh':
            i.attrib['host'] = 's{}.wly.lehaihai.uqeegame.com'.format(sid.lstrip('0'))
        if platform == '1k2k':
            i.attrib['host'] = 's{}.wly.1k2k.com'.format(sid.lstrip('0'))
        if platform == '2686':
            i.attrib['host'] = 's{}.wly.2686.com'.format(sid.lstrip('0'))
        if platform == 'qq990':
            i.attrib['host'] = 's{}.wly.qq990.com'.format(sid.lstrip('0'))
        if platform == 'lqw':
            i.attrib['host'] = 's{}.wly.snsfun.com'.format(sid.lstrip('0'))
        if platform == '5qwan':
            i.attrib['host'] = 's{}.wly.5qwan.com'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8")
    for i in tree.iter(tag="GameEvent"):
        if platform == '1k2k':
            i.attrib['url'] = 'http://s{}.wly.1k2k.com:9103/player/state'.format(sid.lstrip('0'))
        if platform == '2686':
            i.attrib['url'] = 'http://s{}.wly.2686.com:9103/player/state'.format(sid.lstrip('0'))
        if platform == 'qq990':
            i.attrib['url'] = 'http://s{}.wly.qq990.com:9103/player/state'.format(sid.lstrip('0'))
        if platform == '5qwan':
            i.attrib['url'] = 'http://s{}.wly.5qwan.com:9103/player/state'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8")
    for i in tree.iter(tag="Main"):
        #i.attrib['title'] = '{}'.format(newtitle)
        #tree.write(xmlfile, encoding="utf-8", xml_declaration=True)
        if platform == '1k2k':
            i.attrib['favname'] = '1k2k卧龙吟双线{}区'.format(sid.lstrip('0'))
            i.attrib['title'] = '双线{}区'.format(sid.lstrip('0'))
        if platform == '2686':
            i.attrib['url'] = 'http://www.2686.com/game.php?id={}'.format(sid.lstrip('0'))
        if platform == 'lehh':
            i.attrib['favname'] = '乐嗨嗨卧龙吟{}区'.format(sid.lstrip('0'))
            i.attrib['title'] = '乐嗨嗨卧龙吟{}区'.format(sid.lstrip('0'))
            i.attrib['welcome'] = '欢迎来到乐嗨嗨《卧龙吟》{}区！'.format(sid.lstrip('0'))
        if platform == 'lqw':
            i.attrib['favname'] = '乐趣网卧龙吟双线{}区'.format(sid.lstrip('0'))
            i.attrib['title'] = '乐趣网卧龙吟双线{}区'.format(sid.lstrip('0'))
            i.attrib['welcome'] = '欢迎来到乐趣网《卧龙吟>》双线{}区！'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8", xml_declaration=True)
    for i in tree.iter(tag="Bug"):
        if platform == 'qq990':
            i.attrib['posturl'] = \
                'http://s{}.wly.qq990.com/redirect?url=http://wlymanager.uqee.com/SendFeedBack'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8")
    for i in tree.iter(tag="GameEvent"):
        if platform == '1k2k':
            i.attrib['url'] = 'http://s{}.wly.1k2k.com:9103/player/state'.format(sid.lstrip('0'))
        if platform == '2686':
            i.attrib['url'] = 'http://s{}.wly.2686.com:9103/player/state'.format(sid.lstrip('0'))
        if platform == 'qq990':
            i.attrib['url'] = 'http://s{}.wly.qq990.com:9103/player/state'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8")
    for i in tree.iter(tag="Main"):
        #i.attrib['title'] = '{}'.format(newtitle)
        #tree.write(xmlfile, encoding="utf-8", xml_declaration=True)
        if platform == '1k2k':
            i.attrib['favname'] = '1k2k卧龙吟双线{}区'.format(sid.lstrip('0'))
            i.attrib['title'] = '双线{}区'.format(sid.lstrip('0'))
        if platform == '2686':
            i.attrib['url'] = 'http://www.2686.com/game.php?id={}'.format(sid.lstrip('0'))
        if platform == 'lehh':
            i.attrib['favname'] = '乐嗨嗨卧龙吟{}区'.format(sid.lstrip('0'))
            i.attrib['title'] = '乐嗨嗨卧龙吟{}区'.format(sid.lstrip('0'))
            i.attrib['welcome'] = '欢迎来到乐嗨嗨《卧龙吟》{}区！'.format(sid.lstrip('0'))
        if platform == 'lqw':
            i.attrib['favname'] = '乐趣网卧龙吟双线{}区'.format(sid.lstrip('0'))
            i.attrib['title'] = '乐趣网卧龙吟双线{}区'.format(sid.lstrip('0'))
            i.attrib['welcome'] = '欢迎来到乐趣网《卧龙吟>》双线{}区！'.format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8", xml_declaration=True)
    for i in tree.iter(tag="Bug"):
        if platform == 'qq990':
            i.attrib['posturl'] = \
                'http://s1035.wly.qq990.com/redirect?url=http://wlymanager.uqee.com/SendFeedBack'\
                .format(sid.lstrip('0'))
        tree.write(xmlfile, encoding="utf-8", xml_declaration=True)

def khbd_xml(xmlfile,sid,newdomain,platform):
    tree = et.parse(xmlfile)
    #更新id
    for i in tree.iter(tag="ServerList"):
        i.attrib['defaultServer'] = '{}'.format(sid)
        tree.write(xmlfile, encoding="utf-8")

    for i in tree.iterfind("FlashplayerVersion/url"):
        i.text = 'http://{}/player.php'.format(newdomain)
        tree.write(xmlfile, encoding="utf-8")
    #更新server节点属性
    for i in tree.iter(tag="Server"):
        i.attrib['backHost'] = '{}'.format(newdomain)
        i.attrib['host'] = '{}'.format(newdomain)
        i.attrib['name'] = '{}'.format(sid)

        if platform == "789hi":
            i.attrib['title'] = '{}服'.format(sid)
            i.attrib['welcome'] = '789hi《葵花宝典》{}服迎您！'.format(sid)
        if platform == "snsfun":
            i.attrib['title'] = '乐趣网《葵花宝典》双线{}区'.format(sid)
            i.attrib['welcome'] = '乐趣网《葵花宝典》双线{}区欢迎您：给您不一样的武侠体验！'.format(sid)
            for i in tree.iterfind("Server/rechargePage"):
                i.text = 'http://www.lequ.com/pay/index/game/17/s/{}/loginuid/'.format(sid)
        if platform == "311wan":
            i.attrib['title'] = '《葵花宝典》双线{}服'.format(sid)
        if platform == "qq990":
            i.attrib['title'] = '葵花宝典'
            i.attrib['welcome'] = '《葵花宝典》欢迎您！'
            for i in tree.iterfind("Server/battle"):
                i.text = 'http://s127.khbd.qq990.com/battle_report.php?report_id='.format(sid)

        tree.write(xmlfile, encoding="utf-8")
    #更新server子节点属性
    for i in tree.iterfind("Server/battle"):
        i.text = 'http://{}/battle_report.php?report_id='.format(newdomain)
        tree.write(xmlfile, encoding="utf-8",xml_declaration=True)

if __name__ == '__main__':
    change_conf()

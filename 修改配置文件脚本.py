import os
import json
import xml.etree.ElementTree as ET


serverlist = {'wly':'lyingdragon2','xtw':'naughty','khbd':'dreamback','mycs':'naruto','mhjh':'legendary','dbtx':'khbd_h5','mx':'mengxin'}


def khbd_change_file(server_file='/home/soidc/khbd_web/config/Server.xml',server_num,pingtai,*args,**kargs):
    os.system('cp /home/soidc/khbd_web/config/Server.xml{,.bak}')
    tree = ET.parse(server_file)
    root = tree.getroot()
    root.attrib['defaultServer'] = str(server_num)
    root.getchildren()[2].getchildren()[0].text = 'http://s{}.khbd.{}.com/player.php'.format(server_num, pingtai)
    root.getchildren()[5].attrib['name'] = str(server_num)
    root.getchildren()[5].attrib['host'] = "s{}.khbd.{}.com".format(server_num, pingtai)
    root.getchildren()[5].attrib['title'] = "乐趣网《葵花宝典》{}区".format(server_num)
    root.getchildren()[5].getchildren()[0].text = ' http://s{}.khbd.{}.com/battle_report.php?report_id= '.format(serverid, pingtai)
    tree.write(server_file, encoding='utf-8')
    return True


def main():
    a = os.popen('hostname')
    gamehostname = a.read().strip('\n')
    serverhead = gamehostname.split('-')[0]
    server_num = str(int(gamehostname.split('-')[2]))
    gamename = serverlist[serverhead]
        if serverhead == 'khbd':
            khbd_change_file(server_num,pingtai)

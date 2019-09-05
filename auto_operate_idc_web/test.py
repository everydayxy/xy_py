
def get_config():
    '''
    hosts_lists，上线机器配置
    1.运营商
    2.备注名
    3.ip地址
    [('lequ', 'lequ-108', '192.168.232.118'), ('lequ', 'lequ-111', '192.168.232.119'), ('lequ', 'lequ-112', '192.168.232.120')]

    free_ip_lists，闲置机器配置
    1.ip地址
    ['192.168.232.118', '192.168.232.119', '192.168.232.120']
    '''

    from configparser import ConfigParser

    config_file = 'change_list'

    config = ConfigParser()
    config.read(config_file,encoding='utf-8')

    add_hosts_lists = config.get('add', 'add_hosts_list')

    free_ip_lists = config.get('free', 'free_ip_list')

    add_hosts_lists = [(x.strip('\'').split()[1].split('-')[0],x.strip('\'').split()[1],x.strip('\'').split()[0]) for x in add_hosts_lists.split(';')]
    free_ip_lists = [ip.strip('\'') for ip in free_ip_lists.split(';')]

    return add_hosts_lists,free_ip_lists

hosts_lists , ip_lists = get_config()
print(hosts_lists , ip_lists)

a = "//div[@class='el-select-dropdown el-popper']/div[1]/div[1]/ul/li/span[contains(text(),'{}')]".format('uqee')
print(a)


import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



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

    gametype = config.get('game','gametype')

    add_hosts_lists = [(x.strip('\'').split()[1].split('-')[0],x.strip('\'').split()[1],x.strip('\'').split()[0]) for x in add_hosts_lists.split(';')]
    free_ip_lists = [ip.strip('\'') for ip in free_ip_lists.split(';')]

    return add_hosts_lists,free_ip_lists,gametype



def login_idc(username,password):
    try:
        driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        driver.find_element_by_xpath("//button").click()
        return True
    except Exception:
        return False

def find_server_by_ip(ip):
    print(driver.current_url)
    # 调出搜索选项栏
    select = driver.find_element_by_xpath("//input[@placeholder='请选择']")
    select.click()
    '''
    点击菜单后选项:
    1.服务器IP
    2.服务编码
    3.资产编码
    4.备注
    '''
    # 调出下拉菜单并点击
    select_locate = driver.find_element_by_xpath("//span[contains(text(),'服务器IP')]")
    time.sleep(1)
    driver.execute_script("arguments[0].click();", select_locate)
    time.sleep(1)
    # 搜索栏中输入需要查询内容
    driver.find_element_by_xpath("//div[@class='search']/div/input").send_keys(ip)
    time.sleep(1)
    # 点击按钮
    driver.find_element_by_xpath("//button").click()

def change_server_status_merge_after():
    '''
    操作步骤:
    1.修改服务器状态为闲置
    2.备注追加'XXX余下'
    3.保存
    '''
    # 点击菜单里的操作按钮

    driver.find_element_by_xpath("//button[@class='el-button el-button--primary el-button--medium el-dropdown-selfdefine']").click()
    time.sleep(1)
    # 调出操作按钮的下拉菜单并点击编辑选项
    '''
    编辑选项 button class: el-button el-button--primary el-button--mini
    删除选项 button class: el-button el-button--danger el-button--mini
    '''
    driver.find_element_by_xpath("//button[@class='el-button el-button--primary el-button--mini']").click()
    time.sleep(1)
    # 调出<<服务器状态>>的下拉菜单并点击
    driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[1]/div[5]/div/div/div/input").click()
    time.sleep(1)
    '''
    这里处理从上架改成闲置的状态
    '''
    driver.find_element_by_xpath("//div[@class='el-select-dropdown el-popper']/div[1]/div[1]/ul/li/span[contains(text(),'闲置')]").click()
    time.sleep(1)
    # 定位到备注输入框
    nick_name = driver.find_element_by_xpath("//form[@class='el-form host-form']/div[2]/div[@class='el-col el-col-16']/div[1]/div[1]/div[1]/input")

    # 清空备注框的用法
    # nick_name.clear()

    # 追加'合余'两个字
    nick_name.send_keys('合余')
    time.sleep(1)
    '''
    点击修改按钮保存
    修改 class : el-button el-button--primary el-button--medium
    充填 class : el-button el-button--default el-button--medium
    '''
    driver.find_element_by_xpath("//form/div[@class='op el-row']/button[@class='el-button el-button--primary el-button--medium']").click()
    time.sleep(1)

def change_server_status_online_gameserver(company,usage,name):
    '''
    1.修改服务器状态为上架
    2.填写运营商名字(找不到就是暂无)
    3.服务类型改成运营
    4.用途改为对应游戏名字
    5.填入服务器运行时间为此刻
    6.备注改为填入游戏名字
    7.保存
    '''
    print(company,usage,name)

    # 点击菜单里的操作按钮

    driver.find_element_by_xpath("//button[@class='el-button el-button--primary el-button--medium el-dropdown-selfdefine']").click()
    time.sleep(1)
    # 调出操作按钮的下拉菜单并点击编辑选项
    '''
    编辑选项 button class: el-button el-button--primary el-button--mini
    删除选项 button class: el-button el-button--danger el-button--mini
    '''
    driver.find_element_by_xpath("//button[@class='el-button el-button--primary el-button--mini']").click()
    time.sleep(1)

    # 刷新页面
    driver.refresh()
    time.sleep(3)

    # 调出<<服务器状态>>的下拉菜单并点击
    driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[1]/div[5]/div/div/div/input").click()
    time.sleep(1)

    #这里处理改成上架的状态
    driver.find_element_by_xpath("//div[@class='el-select-dropdown el-popper']/div[1]/div[1]/ul/li/span[contains(text(),'上架')]").click()
    time.sleep(1)



    # 运营商点击下拉菜单
    #driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[1]/div[6]/div/div/div/input").send_keys(company)
    driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[1]/div[6]/div/div/div/input").click()
    time.sleep(3)

    # 填写运营商信息
    company_xpath = "//div[@class='el-select-dropdown el-popper']/div[1]/div[1]/ul/li/span[text()='{}']".format(company)
    print(company_xpath)
    element_company = driver.find_element_by_xpath(company_xpath)
    driver.execute_script("arguments[0].click();", element_company)
    time.sleep(2)

    # 点击运营状态下拉菜单
    driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[2]/div[5]/div/div/div/input").click()
    time.sleep(1)

    # 修改运营状态为运营中
    driver.find_element_by_xpath("//div[@class='el-select-dropdown el-popper']/div[1]/div[1]/ul/li/span[text()='运营']").click()
    time.sleep(1)

    # 点击游戏用途下拉菜单
    driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[2]/div[6]/div/div/div/input").click()
    time.sleep(1)

    # 修改运营状态为所选游戏
    element_game = driver.find_element_by_xpath("//div[@class='el-select-dropdown el-popper']/div[1]/div[1]/ul/li/span[text()={}]".format(gametype))
    driver.execute_script("arguments[0].click();", element_game)
    time.sleep(2)

    # 选择日期时间下拉菜单
    driver.find_element_by_xpath("//form[@class='el-form host-form']/div[1]/div[3]/div[6]/div[1]/div[1]/input").click()
    time.sleep(1)

    # 修改开服时间为此刻
    driver.find_element_by_xpath("//div[@class='el-picker-panel el-date-picker el-popper has-time']/div[@class='el-picker-panel__footer']/button").click()
    time.sleep(1)

    # 定位到备注输入框
    nick_name = driver.find_element_by_xpath("//form[@class='el-form host-form']/div[2]/div[@class='el-col el-col-16']/div[1]/div[1]/div[1]/input")

    # 清空备注框的用法
    nick_name.clear()

    # 追加填入备注
    nick_name.send_keys('{}'.format(name))
    time.sleep(1)
    '''
    点击修改按钮保存
    修改 class : el-button el-button--primary el-button--medium
    充填 class : el-button el-button--default el-button--medium
    '''
    driver.find_element_by_xpath("//form/div[@class='op el-row']/button[@class='el-button el-button--primary el-button--medium']").click()

    time.sleep(1)


def operate_merge_after(ip_list):
    '''
    合余闲置服务器操作流程
    '''
    #ip_list = '192.168.232.118,192.168.232.119,192.168.232.120'
    for ip in ip_list:
        time.sleep(2)
        print(ip)
        find_server_by_ip(ip)
        driver.find_element_by_xpath("//div[@class='search']/div/input").clear()
        time.sleep(2)
        change_server_status_merge_after()

def operate_online_server(hosts_lists):
    from company_info import company_info

    COMPANY_DICT = company_info()

    for host in hosts_lists:
        company, nickname, ip = host
        print(company, nickname, ip)
        time.sleep(2)
        find_server_by_ip(ip)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@class='search']/div/input").clear()
        time.sleep(2)
        change_server_status_online_gameserver(company=COMPANY_DICT.get(company, '暂无'), usage=gametype,name=nickname)


if __name__ == '__main__':

    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver.get('http://g.uqee.com/idc/login')

    time.sleep(3)

    USERNAME = ''
    PASSWORD = ''

    hosts_lists, ip_lists, gametype = get_config()

    # hosts_lists 上架服务器信息
    # ip_lists  闲置服务器信息
    # gametype 上架服务器类型

    if not login_idc(USERNAME,PASSWORD):
        print('login error')
        sys.exit(1)

    print(hosts_lists, ip_lists, gametype)

    # 合余操作函数调用
    # operate_merge_after(ip_lists)

    # 上线操作函数调用
    operate_online_server(hosts_lists)

    driver.quit()
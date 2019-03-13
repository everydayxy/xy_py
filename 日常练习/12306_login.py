import requests
import json
import getpass

class Login():
    '''
    初始化操作
    '''
    def __init__(self):
        # 模拟浏览器请求头
        self.agent_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
        # 建立会话对象
        self.session = requests.session()

    def get_authentication_photo(self):
        '''
        下载验证码的图片
        '''
        photo_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
        # 请求验证码url并返回结果
        response = self.session.get(url=photo_url, headers=self.agent_header, verify=False)
        with open('image.jpg','wb') as f:
            f.write(response.content)
        print('请到脚本执行同路径去看image.jpg这个文件')

    def Check_Authentication_Code(self):
        view_location = ['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']
        check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        # =======================================================================
        # 根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置，例如：2,4
        # ---------------------------------------
        #         |         |         |
        #    0    |    1    |    2    |     3
        #         |         |         |
        # ---------------------------------------
        #         |         |         |
        #    4    |    5    |    6    |     7
        #         |         |         |
        # ---------------------------------------
        ret = {str(idx):location for idx,location in enumerate(view_location)}
        # print(ret)
        user_idx = input('请输入图片索引号，以逗号分隔(例子：2,4): ')
        user_str = ''
        for x in user_idx.split(','):
            user_str += '{},'.format(ret[x])
        user_str = user_str[0:-1]
        verify_location = ','.join(user_str.split(','))
        data = {
            'login_site': 'E',  # 固定的
            'rand': 'sjrand',  # 固定的
            'answer': verify_location  # 验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }
        # print(data)
        content = self.session.post(url=check_url, data=data, headers=self.agent_header, verify=False)
        result_dic = json.loads(content.content)
        code = result_dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        # print(code)
        if int(code) == 4:
            return True
        else:
            return False

    def main_login(self):
        username = input('Please input your UserName:')
        psswd = getpass.getpass('Please input your Password:')
        loginurl = "https://kyfw.12306.cn/passport/web/login"
        data = {
            'username': username,
            'password': psswd,
            'appid': 'otn'
        }
        result = self.session.post(url=loginurl, data=data, headers=self.agent_header, verify=False)
        result_dic = json.loads(result.content)
        msg = result_dic['result_message']
        # 结果的编码方式是Unicode编码，所以对比的时候字符串前面加u,或者mes.encode('utf-8') == '登录成功'进行判断，否则报错
        if msg == '登录成功':
            print('恭喜你，登录成功，可以购票!')
        else:
            print('对不起，登录失败，请检查登录信息!')

if __name__ == '__main__':
    print('程序开始啦！！！！')
    login = Login()
    login.get_authentication_photo()
    flag = login.Check_Authentication_Code()
    print(flag)
    if flag:
        login.main_login()
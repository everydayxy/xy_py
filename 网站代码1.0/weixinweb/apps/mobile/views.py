# coding:utf8

import json
import sys
import urllib
from datetime import datetime
import logging

import requests
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View

from models import MobileInfo, OperationLog

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('django')

# 获得token
def get_token():
    corpid = 'ww867aa77107c43f7b'
    corpsecret = 'D2oxoqAvl2Q67-PXOsMMcu-p01SooQrnVoAz4nswXiM'
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(corpid, corpsecret)
    mydict = requests.get(url).json()
    return mydict['access_token']

#获取用户名
def get_member(code):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={}&code={}'.format(token, code)
    return requests.get(url).content

# 获取用户详细信息
def get_member_info(username):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={}&userid={}'.format(token, username)
    return requests.get(url).content

# 向用户发送消息
def sendinfo(username, content):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(token)
    data = {
               "touser": "{}".format(username),
               "toparty": "",
               "totag": "",
               "msgtype": "text",
               "agentid": 1000021,
               "text": {
                   "content": "{} ".format(content)
               },
               "safe": 0
        }
    return requests.post(url, json=data)

class LoginView(View):

    def get(self, request):
        corpid = 'ww867aa77107c43f7b'
        agentid = '1000021'
        redirect = urllib.quote('http://phone.uqee.com')
        url = "https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid={}&agentid={}&redirect_uri={}".format(corpid, agentid, redirect)
        return HttpResponseRedirect(url)

class IndexView(View):
    # 首页
    def get(self, request):
        all_mobile = MobileInfo.objects.all()
        # 设备型号
        all_mobile_type = MobileInfo.objects.values("mobile_type").annotate(dcount=Count("mobile_type"))
        # 设备分类
        all_types = MobileInfo.objects.values("type").annotate(dcount=Count("type"))
        # 微信用户
        code = request.GET.get('code', '')
        if code:
            userdict = json.loads(get_member(code))
            if userdict['errcode'] == 0:
                username = userdict['UserId']
                user = authenticate(username=username, password='love.1993')
                # 判断用户信息是否注册如果没有就自动注册
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        logger.info('用户[{}]登录成功!'.format(user))
                    return HttpResponseRedirect(reverse('index'))
                else:
                    userdict = json.loads(get_member_info(username))  # 根据用户名获取用户的中文名字
                    if userdict['errcode'] == 0:
                        user_hans = userdict['name']
                        users = User()
                        # User.objects.get_or_create(username=username, password=make_password('love.1993'), first_name=user_hans)
                        # User.save()
                        users.username = username
                        users.password = make_password('love.1993')
                        users.first_name = user_hans
                        users.save()
                        user = authenticate(username=username, password='love.1993')
                        login(request, user)
                        return HttpResponseRedirect(reverse('index'))
                    else:
                        return render(request, '404.html', {'msg': '未能从企业微信获取到用户中文名称'})
            else:
                return render(request, '404.html', {'msg': '未能从企业微信获取到用户信息'})
        # 用户未注册踢到登录页
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        # 按设备型号分类
        mobile_type = request.GET.get('mobile_type', '')
        if mobile_type:
            all_mobile = all_mobile.filter(mobile_type=mobile_type)
        # 按设备类型
        type = request.GET.get('type', '')
        if type:
            all_mobile = all_mobile.filter(type=type)
        # 按使用状态分类
        state = request.GET.get('state', '')
        if state:
            all_mobile = all_mobile.filter(mobile_state=state)
        return render(request, 'index.html', {
            'all_mobile': all_mobile,
            'all_mobile_type': all_mobile_type,
            'all_types': all_types,
        })

class ShenQing(View):
    def get(self, request):
        # 获取设备类型
        types = request.GET.get('type', '')
        # 获取设备型号
        mobile_type = request.GET.get('mobile_type', '')
        # 获取设备颜色
        color = request.GET.get('color', '')
        # 获取设备编码
        number = request.GET.get('number', '')
        # 获取设备SN码
        sn = request.GET.get('sn', '')
        # 获取登录用户
        user = request.user
        # 获取本次使用用户
        mobile_current_user = request.GET.get('current_user', '')
        # 获取当前账户的用户名
        curentusernamedict = json.loads(get_member_info(user))  # 根据用户名获取用户的中文名字
        if curentusernamedict['errcode'] == 0:
            curent_username = curentusernamedict['name']
            if mobile_current_user:
                content = u'{}正在申请使用设备，设备类型：{}，设备型号：{}，设备颜色：{}，设备SN码：{}，申请时间：{}，' \
                          u'<a href="http://phone.uqee.com/queren/?state=yes&sn={}&curent_username={}&mobile_current_user={}">同意</a>，' \
                          u'或者是<a href="http://phone.uqee.com/queren/?state=no&sn={}&curent_username={}&mobile_current_user={}">不同意</a>'.format(
                          curent_username, types, mobile_type, color, sn, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          sn, curent_username, mobile_current_user, sn, curent_username, mobile_current_user)
                logger.info(content)
                try:
                    # 根据用户名推送微信消息
                    curent_username = request.GET.get('current_user', '')
                    user = User.objects.get(first_name=curent_username).username
                    sendinfo(user, content.encode('utf8'))
                    # sendinfo("sunyange", content.encode('utf8'))
                    return HttpResponseRedirect(reverse('index'))
                except:
                    return render(request, '404.html', {'msg': '推送微信信息失败！'})
            else:
                MobileInfo.objects.filter(sn=sn).update(current_user=str(curent_username),
                                                        last_user=str(mobile_current_user),
                                                        update_time=datetime.now(), mobile_state='use')
                content = u'{}正在申请使用设备，设备类型：{}，设备型号：{}，设备颜色：{}，设备SN码：{}，申请时间：{}'.format(
                    curent_username, types, mobile_type, color, sn, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                opt = OperationLog()
                opt.user = curent_username
                opt.operation = '申请'
                opt.entity = u'设备类型：{}，设备型号：{}，设备颜色：{}，设备SN码：{}'.format(types, mobile_type, color, sn)
                opt.save()
                logger.info(content)
                try:
                    # 根据用户名推送微信消息
                    sendinfo(user, content.encode('utf8'))
                    # sendinfo("sunyange", content.encode('utf8'))
                    return HttpResponseRedirect(reverse('index'))
                except:
                    return render(request, '404.html', {'msg': '推送微信信息失败！'})
        else:
            return HttpResponseRedirect(reverse('login'))


class GuiHuan(View):
    def get(self, request):
        # 获取手机型号
        sn = request.GET.get('sn', '')
        # 获取本次使用用户
        mobile_current_user = request.GET.get('current_user', '')
        # 获取本次使用用户
        user = request.user
        # 发送提醒消息给用户
        usernamedict = json.loads(get_member_info(user))  # 根据用户名获取用户的中文名字
        # if usernamedict['errcode'] == 0:
        #     username = usernamedict['name']
        #     content = u'{}正在归还手机，手机型号为：{}'.format(username, mobile_type)
        #     try:
        #         sendinfo(user, content.encode('utf8'))  # 根据用户名推送微信消息
        #         return HttpResponseRedirect(reverse('index'))
        #     except:
        #         return render(request, '404.html', {'msg': '推送微信信息失败！'})
        # else:
        #     return render(request, '404.html', {'msg': usernamedict['errmsg']})
        if usernamedict['name'] != u'孙彦阁':
            return render(request, '404.html', {'msg': '权限不够，请联系管理员！'})
        # 更新信息
        MobileInfo.objects.filter(sn=sn).update(update_time=datetime.now(), current_user=u'孙彦阁', last_user=str(mobile_current_user),  mobile_state='free')
        return HttpResponseRedirect(reverse('index'))


class QueRen(View):
    def get(self, request):
            state = request.GET.get('state', '')
            sn = request.GET.get('sn', '')
            curent_username = request.GET.get('curent_username', '')
            user = User.objects.get(first_name=curent_username).username
            if not state and sn:
                return render(request, '404.html', {'msg': '地址错误！'})
            if state == 'yes':
                mobile_current_user = request.GET.get('mobile_current_user', '')
                MobileInfo.objects.filter(sn=sn).update(current_user=str(curent_username),
                                                        last_user=str(mobile_current_user),
                                                        update_time=datetime.now(),
                                                        mobile_state='use')
                mobileinfo = MobileInfo.objects.get(sn=sn)
                opt = OperationLog()
                opt.user = curent_username
                opt.operation = '申请'
                opt.entity = u'设备类型：{}，设备型号：{}，设备颜色：{}，设备SN码：{}'.format(mobileinfo.type, mobileinfo.mobile_type, mobileinfo.color, sn)
                opt.save()
                logger.info(u'申请[ 设备类型：{}，设备型号：{}，设备颜色：{}，设备SN码：{} ]通过'.format(mobileinfo.type, mobileinfo.mobile_type, mobileinfo.color, sn))
                return render(request, '404.html', {'msg': '你同意了对方的请求！'})
            elif state == 'no':
                sendinfo(user, '对方拒绝了你的申请！')
                return render(request, '404.html', {'msg': '你拒绝了对方的请求！'})
            else:
                return render(request, '404.html', {'msg': '传入参数错误！'})

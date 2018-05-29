# coding:utf8

from django.conf.urls import url


from views import IndexView, LoginView, ShenQing, GuiHuan, QueRen

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^shenqing/', ShenQing.as_view(), name='shenqing'),
    url(r'^guihuan/', GuiHuan.as_view(), name='guihuan'),
    url(r'^queren/', QueRen.as_view(), name='queren'),

]
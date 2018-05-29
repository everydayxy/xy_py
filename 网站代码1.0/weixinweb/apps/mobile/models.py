# coding:utf8

from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class MobileInfo(models.Model):
        current_user = models.CharField(verbose_name=u'当前正在使用的用户', max_length=20, blank=True, null=True)
        last_user = models.CharField(verbose_name=u'上一次使用的用户', max_length=20, blank=True, null=True)
        mobile_type = models.CharField(verbose_name=u'设备名称', max_length=50, blank=True, null=True)
        type = models.CharField(verbose_name=u'设备分类', max_length=50, blank=True, null=True)
        number = models.CharField(verbose_name=u'设备型号', max_length=50, blank=True, null=True)
        color = models.CharField(verbose_name=u'设备颜色', max_length=20, blank=True, null=True)
        sn = models.CharField(verbose_name=u'设备SN码', max_length=100, blank=True, null=True, unique=True)
        mobile_state = models.CharField(verbose_name=u'手机状态', choices=(('use', '使用'), ('free', '空闲')), max_length=20, default=u'free')
        remark = models.TextField(verbose_name=u'备注', blank=True, null=True)
        update_time = models.DateTimeField(verbose_name=u'更新时间', default=datetime.now)

        class Meta:
            verbose_name = '设备借用记录'
            verbose_name_plural = verbose_name

        def __unicode__(self):
            return self.mobile_type


class OperationLog(models.Model):
        user = models.CharField(verbose_name=u'操作用户', max_length=20)
        operation = models.CharField(verbose_name=u'操作', max_length=20)
        entity = models.CharField(verbose_name=u'操作实体', max_length=100)
        operation_date = models.DateTimeField(verbose_name=u'操作发生时间', default=datetime.now)

        class Meta:
            verbose_name = '设备借用日志记录'
            verbose_name_plural = verbose_name


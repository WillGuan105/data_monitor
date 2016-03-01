#!/usr/bin/env python
#!coding:utf-8
from django.db import models

# Create your models here.

class PayResult(models.Model):
    jobid=models.CharField(max_length=200,verbose_name=u'工单号')
    result=models.CharField(max_length=200,verbose_name=u'运行结果')
    author=models.CharField(max_length=200,verbose_name=u'执行人')
    env=models.CharField(max_length=200,verbose_name=u'执行环境')
    ctime=models.CharField(max_length=200,verbose_name=u'创建时间')
    etime=models.CharField(max_length=200,verbose_name=u'结束时间')

#!/usr/bin/env python
#!coding:utf-8
from django.db import models

# Create your models here.

class Modules(models.Model):
	m_id=models.IntegerField(primary_key=True)
	m_name=models.CharField(max_length=100,verbose_name=u'模块名字')

	def __unicode__(self):
		return str(self.m_name)

class Interface(models.Model):
	i_ID=models.IntegerField(primary_key=True)
	i_name=models.CharField(max_length=200,verbose_name=u'接口名字')
	i_params=models.CharField(max_length=500,verbose_name=u'请求参数')
	i_module=models.ForeignKey(Modules)
	i_status=models.CharField(max_length=200,verbose_name=u'结果状态')

	def __unicode__(self):
		return "%s %s" % (self.i_ID,self.i_name)

class runResult(models.Model):
	his_id=models.IntegerField(verbose_name=u'报表结果id')
	intf=models.ForeignKey(Interface)
	status=models.CharField(max_length=200,verbose_name=u'运行结果状态')
	error_request=models.CharField(max_length=500,verbose_name=u'报错的请求')

	def __unicode__(self):
		return str(self.his_id)

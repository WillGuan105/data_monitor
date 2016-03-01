#!/usr/bin/env python
#!coding:utf-8
from django.db import models

class FakecubeIF(models.Model):
	f_id=models.IntegerField(unique=True, verbose_name=u'Fakecube接口id')
	f_name=models.CharField(max_length=300,verbose_name=u'Fakecube接口name')
	frun_url=models.TextField(verbose_name=u'查询接口数据的url')
	f_status=models.CharField(max_length=200,verbose_name=u'运行结果状态')

	def __unicode__(self):
		return str(self.f_id)
		#return self.f_name

#Fakecube接口运行结果
class FakecubeIFResult(models.Model):
	fresult_id=models.IntegerField(verbose_name=u'Fakecube接口结果id')
	f_id=models.ForeignKey(FakecubeIF)
	f_status=models.CharField(max_length=200,verbose_name=u'运行结果状态')

	def __unicode__(self):
		return str(self.fresult_id)
#!/usr/bin/env python
#!coding:utf-8
from django.db import models
import sys

# Create your models here.
class checkDiffItems(models.Model):
	c_ID=models.IntegerField(unique=True, verbose_name=u'检测同商品接口id', blank=False, primary_key=True)
	c_name=models.CharField(max_length=200,verbose_name=u'名字', blank=False)
	c_type=models.CharField(default='null',max_length=200,verbose_name=u'平台类型（pc或mob）')
	c_baseurl=models.CharField(max_length=200,verbose_name=u'请求url http://', blank=False)
	c_params=models.CharField(max_length=500,verbose_name=u'请求参数',blank=False)
	c_path=models.CharField(max_length=200,verbose_name=u'至twitter_id路径')
	c_otherparams=models.CharField(default='["null"]',max_length=200,verbose_name=u'其他需要解析的json列表字段（如分页等）')

	def __unicode__(self):
		return str("%d %s %s" % (self.c_ID,self.c_name,self.c_baseurl))
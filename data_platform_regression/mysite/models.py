#!/usr/bin/env python
#!coding:utf-8

from django.db import models

#报表
class Report(models.Model):
	r_id=models.IntegerField(unique=True, verbose_name=u'报表id')
	r_name=models.CharField(max_length=200,verbose_name=u'报表名字')
	status=models.CharField(max_length=200,verbose_name=u'运行结果状态')
	
	def __unicode__(self):
		return str(self.r_id)

#图表
class Graph(models.Model):
	g_id=models.IntegerField(unique=True, verbose_name=u'图表id')
	g_name=models.CharField(max_length=200,verbose_name=u'图表name')
	run_url=models.TextField(verbose_name=u'查询图表数据的url')
	rep_id=models.ForeignKey(Report)
	status=models.CharField(max_length=200,verbose_name=u'运行结果状态')

	def __unicode__(self):
		return str(self.g_id)

#报表运行结果
class ReportResult(models.Model):
	result_id=models.IntegerField(verbose_name=u'报表结果id')
	r_id=models.ForeignKey(Report)
	status=models.CharField(max_length=200,verbose_name=u'运行结果状态')

#图表运行结果
class GraphResult(models.Model):
	result_id=models.IntegerField(verbose_name=u'图表结果id')
	g_id=models.ForeignKey(Graph)
	status=models.CharField(max_length=200,verbose_name=u'运行结果状态')

	def __unicode__(self):
		return str(self.result_id)



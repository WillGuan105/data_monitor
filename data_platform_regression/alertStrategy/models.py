#!/usr/bin/env python
#!coding:utf-8
from django.db import models
import sys

# Create your models here.

class alertRecord(models.Model):
	a_ID=models.IntegerField(unique=True, verbose_name=u'报警接口id', blank=False)
	a_name=models.CharField(max_length=200,verbose_name=u'名字', blank=False)
	a_class=models.CharField(max_length=200,verbose_name=u'接口所属类别Groupon,focus,data', blank=False)
	a_plat=models.CharField(max_length=200,verbose_name=u'平台pc,mob', blank=False)
	a_city=models.CharField(max_length=200,verbose_name=u'城市北京,广州', blank=False)
	a_createTime=models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=u'报警记录创建时间', blank=False)
	a_mailTimes=models.IntegerField(default=0, verbose_name=u'报警邮件发送次数')
	a_msgTimes=models.IntegerField(default=0, verbose_name=u'报警短信发送次数')
	a_alertTimes=models.IntegerField(default=0, verbose_name=u'报警次数')
	a_errorType=models.CharField(max_length=200,verbose_name=u'错误类型')

	def __unicode__(self):
		return str(self.a_ID)


class alertReport(models.Model):
	reload(sys)
	sys.setdefaultencoding('utf8')
	r_interfaceName=models.CharField(max_length=200,verbose_name=u'接口名字', blank=False)
	r_class=models.CharField(max_length=200,verbose_name=u'接口所属类别Groupon,focus,data', blank=False)
	r_plat=models.CharField(max_length=200,verbose_name=u'平台pc,mob', blank=False)
	r_city=models.CharField(max_length=200,verbose_name=u'城市北京,广州', blank=False)
	r_createTime=models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=u'报警记录创建时间', blank=False)
	r_alertTimes=models.IntegerField(default=0, verbose_name=u'报警次数')
	r_duration=models.CharField(max_length=200,verbose_name=u'错误持续时间', blank=False)
	r_traceUsers=models.CharField(max_length=200,verbose_name=u'问题跟踪人')
	r_comments=models.CharField(max_length=200,verbose_name=u'备注', default="null")

	def __unicode__(self):
		return str("%d %s" % (self.id,self.r_interfaceName))


class monitorItems(models.Model):
	m_active=models.CharField(max_length=200,verbose_name=u'是否可用', blank=False)
	m_name=models.CharField(max_length=200,verbose_name=u'名字', blank=False)
	m_class=models.CharField(max_length=200,verbose_name=u'接口所属类别Groupon,focus,data', blank=False)
	m_url=models.CharField(max_length=200,verbose_name=u'请求url http://', blank=False)
	m_params=models.CharField(max_length=500,verbose_name=u'请求参数',blank=False)
	m_host=models.CharField(max_length=200,verbose_name=u'host -H "host:"',blank=False)
	m_plat=models.CharField(max_length=200,verbose_name=u'平台pc,mob', blank=False)
	m_city=models.CharField(max_length=200,verbose_name=u'城市北京,广州', blank=False)
	m_expStr=models.CharField(max_length=200,verbose_name=u'预期返回值')
	m_expDetailStr=models.CharField(max_length=200,verbose_name=u'预期详细返回值')
	m_alertUsers=models.CharField(max_length=200,verbose_name=u'报警接收人',blank=True)
	#m_alertGroupID=models.CharField(max_length=200,verbose_name=u'报警接收组id',blank=True,null=True)
	m_interval=models.IntegerField(default=1, verbose_name=u'任务运行频率', help_text='以min为单位,默认为1')
	m_status=models.CharField(default='not useful',max_length=200,verbose_name=u'当前状态')

	def __unicode__(self):
		return str("%d %s %s" % (self.id,self.m_name,self.m_url))

class alertUsersGroups(models.Model):
	#g_ID=models.IntegerField(unique=True, verbose_name=u'报警组id', blank=False, primary_key=True)
	g_class=models.CharField(unique=True,default='null',max_length=200,verbose_name=u'报警组类别', blank=False, primary_key=True)
	g_name=models.CharField(max_length=200,verbose_name=u'名字', blank=False)
	g_alertUsers=models.CharField(max_length=200,verbose_name=u'报警接收组成员')
	g_disturb=models.CharField(max_length=200,default='False',verbose_name=u'是否打扰',blank=False)

	def __unicode__(self):
		return str("%s %s %s %s" % (self.g_class,self.g_name,self.g_alertUsers,self.g_disturb))

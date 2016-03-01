# -*-coding:utf-8 -*-

import os,sys
import logging
from django.db.models import Q
from datetime import *
from datetime import timedelta
from .models import *
from Monitor import Monitor
from django.core.exceptions import ObjectDoesNotExist
import pytz
import json
import ConfigParser
import threadpool


class commonMethod:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.config_file= "%s/alertStrategy/conf/domain_conf.ini" % self.BASE_DIR
		self.report_token="566f8362d435f"

	def formatTime(self,ftime):
		timeStr=ftime.split(".")[0]
		time_arr=timeStr.split(":")
		for da in range(0,len(time_arr)):
			if len(time_arr[da])<2:
				time_arr[da]='0'+time_arr[da]
		timeStr=":".join(time_arr)
		return timeStr

	def getValueOfPath(self,reJson,path):
		if not reJson:
			return 0
		pArr=path.split("#")
		valStr="reJson"
		for p in pArr:
			if p.isdigit():
				valStr+="[%s]" % p
			else:
				p=p.strip("'")
				valStr+="['%s']" % p
		try:
			valStr=eval(valStr)
		except:
			return "exception"
		if type(valStr)==int:
			valStrLen=len(str(valStr))
		else:
			valStrLen=len(valStr)
		#logger.info("valStrLen: %s" % valStrLen)
		return valStrLen

	def calDuration(self,cid):
		ardOps=alertRecordOps()
		arObj=ardOps.getRecordObject(cid)
		#arObj = alertRecord.objects.get(a_ID=id)
		now=datetime.now()
		print now
		crtime=arObj.a_createTime
		if not crtime:
			duration = str(now)
		else:
			lasttimes = crtime
			lasttimes = lasttimes.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
			lasttimes = lasttimes.replace(tzinfo=None)
			duration = str(now - lasttimes)
		#print duration
		return duration

	def getFormatCurTime(self):
		cur_time=datetime.now()
		cur_time = str(cur_time)
		cur_time = cur_time.replace(' ', '_')
		cur_time = self.formatTime(cur_time)
		return cur_time

	def getStrategyConstant(self,key):
		conf=ConfigParser.ConfigParser()
		conf.read(self.config_file)
		re_value=conf.get('alertStrategy',key)
		return re_value

	def getHostConf(self,key):
		conf=ConfigParser.ConfigParser()
		conf.read(self.config_file)
		re_value=conf.get('hostConf',key)
		return re_value

	def getLogger(self):
		logger = logging.getLogger('alertStrategy')
		FILE=os.path.join(self.BASE_DIR,'log')
		fh = logging.FileHandler(os.path.join(FILE,'Monitor.log'))
		formatter = logging.Formatter('%(asctime)s -  %(filename)s[line:%(lineno)d]－%(name)s - %(levelname)s %(levelno)s : %(message)s')
		fh.setFormatter(formatter)
		logger.setLevel(logging.INFO)
		if logger.handlers:
			logger_len=len(logger.handlers)
			for i in range(0,logger_len):
				logger.handlers.pop(0)
		logger.addHandler(fh)
		return logger

class alertRecordOps:
	def __init__(self):
		self.cm=commonMethod()
		self.logger=self.cm.getLogger()
		pass

	def updateMailTimes(self,cid):
		try:
			arObj=alertRecord.objects.get(a_ID=cid)
			arObj.a_mailTimes = arObj.a_mailTimes +1
			arObj.save()
		except ObjectDoesNotExist:
			self.logger.exception("updateMailTimes get object does not exist")
			pass

	def updateErrorType(self,cid,errorType):
		arObj=self.getRecordObject(cid)
		arObj.a_errorType=errorType
		arObj.save()

	def updateAlertTimes(self,cid):
		arObj=self.getRecordObject(cid)
		arObj.a_alertTimes+=1
		arObj.save()

	def updateMsgTimes(self,cid):
		try:
			arObj=alertRecord.objects.get(a_ID=cid)
			#arObj=self.getRecordObject(id)
			arObj.a_msgTimes = arObj.a_msgTimes +1
			# arObj.a_lastMsgTimes = datetime.now()
			arObj.save()
		except ObjectDoesNotExist:
			self.logger.exception("updateMsgTimes get object does not exist")
			pass

	# def updateAlertTimes(self,cid):
	# 	try:
	# 		arObj=alertRecord.objects.get(a_ID=cid)
	# 		#arObj=self.getRecordObject(id)
	# 		arObj.a_msgTimes = arObj.a_alertTimes +1
	# 		# arObj.a_lastMsgTimes = datetime.now()
	# 		arObj.save()
	# 	except ObjectDoesNotExist:
	# 		self.logger.exception("updateMsgTimes get object does not exist")
	# 		pass
	def getRecordItems(self):
		return alertRecord.objects.filter(a_alertTimes__gte=3)

	def getRecordObject(self,cid):
		try:
			ar = alertRecord.objects.get(a_ID=cid)
			return ar
		except ObjectDoesNotExist:
			# self.logger.exception("getRecordObject get object does not exist")
			return None

	def addRecord(self,c_id, c_name,c_class,c_plat, c_city,c_createTime, c_mailTimes=0, c_msgTimes=0, c_alertTimes=0, c_errorType=''):
		ar=alertRecord(a_ID=c_id,a_name=c_name,a_class=c_class,a_plat=c_plat,a_city=c_city,a_createTime=c_createTime,a_mailTimes=c_mailTimes,a_msgTimes=c_msgTimes,a_alertTimes=c_alertTimes,a_errorType=c_errorType)
		ar.save()

	# def isRecordExist(self,id):
	# 	try:
	# 		r = alertRecord.objects.get(a_ID=id)
	# 		return True
	# 	except ObjectDoesNotExist:
	# 		#self.logger.exception("isRecordExist get object does not exist")
	# 		return False

	def deleteRecord(self,cid):
		try:
			r = alertRecord.objects.get(a_ID=cid)
			r.delete()
		except ObjectDoesNotExist:
			#self.logger.exception("deleteRecord get object does not exist")
			pass

class alertMailAndMsg:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.cm=commonMethod()
		self.ardOps=alertRecordOps()
		self.logger=self.cm.getLogger()
		self.MAX_SEND_MAILS=int(self.cm.getStrategyConstant('max_send_mails'))
		self.MAX_SEND_MSGS=int(self.cm.getStrategyConstant('max_send_msgs'))
		self.MAX_ALERTS_MAIL=int(self.cm.getStrategyConstant('max_alerts_mail'))
		self.MAX_ALERTS_MSG=int(self.cm.getStrategyConstant('max_alerts_msg'))
		self.NO_MSG_DAY=int(self.cm.getStrategyConstant('no_msg_day'))
		self.NO_MSG_NIGHT=int(self.cm.getStrategyConstant('no_msg_night'))
		self.MAX_DOWN_TIME=int(self.cm.getStrategyConstant('max_down_time'))
		self.msgInterval = timedelta(seconds=self.MAX_DOWN_TIME)

	def checkTime(self):
		nowhour = datetime.now().hour
		isNight = False
		if nowhour >= self.NO_MSG_NIGHT or nowhour <= self.NO_MSG_DAY:
			isNight = True
		return isNight

	def ifSendMail(self,a_ID):
		arObj=self.ardOps.getRecordObject(a_ID)
		if arObj.a_mailTimes >= self.MAX_SEND_MAILS:
			return False
		return True

	def ifSendMsg(self,a_ID):
		miObj=monitorItems.objects.get(id=a_ID)
		mclass=miObj.m_class.lower()
		agObj=alertUsersGroups.objects.get(g_class=mclass)
		if agObj.g_disturb == 'False':
			if self.checkTime():
				return False

		arObj=self.ardOps.getRecordObject(a_ID)

		if not arObj:
			return False

		if arObj.a_mailTimes < self.MAX_SEND_MAILS:
			return False

		if arObj.a_msgTimes >= self.MAX_SEND_MSGS:
			return  False

		return True

	def ifMeetMsgInterval(self,arObj):
		now=datetime.now()
		if not arObj.a_createTime:
			return False

		crtimes = arObj.a_createTime
		crtimes = crtimes.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
		crtimes = crtimes.replace(tzinfo=None)

		if arObj.a_createTime and now-crtimes > self.msgInterval:
			return True
		return False

	def getAlertType(self,a_ID):
		if not self.ifSendMsg(a_ID) and not self.ifSendMail(a_ID):
			self.logger.info("ifSendMsg mail None")
			return None

		arObj=self.ardOps.getRecordObject(a_ID)
		if not arObj:
			self.logger.info("None arObj None")
			return None
		if arObj.a_mailTimes >= self.MAX_SEND_MAILS and arObj.a_msgTimes >= self.MAX_SEND_MSGS:
			self.logger.info("ifSendMsg mail times>0")
			return None

		if self.ifMeetMsgInterval(arObj) and self.ifSendMsg(a_ID):
			return "msg"

		if arObj.a_alertTimes >= self.MAX_ALERTS_MAIL and self.ifSendMail(a_ID):
			return "mail"
		if arObj.a_alertTimes >= self.MAX_ALERTS_MSG and self.ifSendMsg(a_ID):
			return "msg"

		self.logger.info("none of above None")
		return None

	def getAllAlertUsers(self,id):
		obj=None
		try:
			obj=monitorItems.objects.get(id=id)
		except Exception,e:
			self.logger.exception(e)
		print "++++++++++++++++++++++++",obj
		if not obj:
			return None
		traceusers =''
		if obj.m_class:
			classlist=obj.m_class.split(',')
			for mc in classlist:
				mc=mc.lower()
				agObj=alertUsersGroups.objects.get(g_class=mc)
				traceusers +=','+agObj.g_alertUsers
		if obj.m_alertUsers:
			traceusers +=','+obj.m_alertUsers
			'''
			tracelist = obj.m_alertUsers.split(',')
			for user in tracelist:
				try:
					gid=int(user)
				except:
					traceusers += ','+ user
					continue
				gobj=alertUsersGroups.objects.get(g_ID=gid)
				traceusers += ','+ gobj.g_alertUsers
			'''
		traceusers=traceusers.strip(',')
		traceusers=traceusers.split(',')
		#去重
		allusers=list(set(traceusers))
		print 'allsusers is %s'%allusers
		print '**********************************'

		return allusers

	def sendAlert(self,id,users,phoneMsg,mailSubj,mailcontent,alerttype):
		phoneMsg=phoneMsg.replace("#",":")
		mailcontent=mailcontent.replace("#",":")
		users=self.getAllAlertUsers(id)
		print "users is ",users
		print "&&&&&&&&&&&&&&&&&&&&&&&&&&&"
		#cmd = """/usr/bin/wget -q "http://smsapi.meilishuo.com/smssys/interface/smsapi.php?smsKey=1407399202710&type=%s&name=%s&phone=&smscontent=%s&mailsubject=%s&mailcontent=%s" -O /dev/null """ % (type,user,phoneMsg,mailSubj,mailcontent)
		send_status_list=[]
		for user in users:
			cmd = """wget -q "http://smsapi.meilishuo.com/smssys/interface/smsapi.php?smsKey=1407399202710&type=%s&name=%s&phone=&smscontent='%s'&mailsubject='%s'&mailcontent='%s'" -O /dev/null """ % (alerttype,user,phoneMsg,mailSubj,mailcontent)
			self.logger.info(cmd)
			re=os.popen(cmd).read()
			if re:
				self.logger.error("Msg: %s send to %s fail !!!" % (phoneMsg,user))
				send_status_list.append('Fail')
			else:
				self.logger.info("Msg send success !!!")
				send_status_list.append('success')
		if send_status_list.__contains__('success'):
			return True
		else:
			return False

class alertReportOps:
	def __init__(self):
		self.cm=commonMethod()
		self.REPORT_DURATION=str(self.cm.getStrategyConstant('report_duration'))
		self.logger=self.cm.getLogger()
		pass

	def updateComments(self,rpid,comments):
		try:
			alertReport.objects.filter(id=rpid).update(r_comments=comments)
		except Exception,e:
			self.logger.exception(e)

	def getAlertReport(self,belong_class,begin_time,end_time):
		belong_class=belong_class.lower()
		dur=self.REPORT_DURATION
		if belong_class=="all":
			aReports=alertReport.objects.filter(Q(r_alertTimes__gte=3) & Q(r_createTime__range=(begin_time,end_time))).order_by('r_createTime').reverse()
		else:
			aReports=alertReport.objects.filter(Q(r_class=belong_class) & Q(r_createTime__range=(begin_time,end_time)) & Q(r_alertTimes__gte=3)).order_by('r_createTime').reverse()
		return aReports

	def addAlertReport(self,c_id,c_interfaceName,c_class,c_plat,c_city,c_createTime,c_alertTimes,c_duration,c_traceUsers,c_comments):
		reload(sys)
		sys.setdefaultencoding('utf8')
		self.logger.info("add %s" % c_interfaceName)
		arp=alertReport(r_interfaceName=c_interfaceName,r_class=c_class,r_plat=c_plat,r_city=c_city,r_createTime=c_createTime,r_alertTimes=c_alertTimes,r_duration=c_duration,r_traceUsers=c_traceUsers,r_comments=c_comments)
		arp.r_interfaceName=str(arp.r_interfaceName)+'/'+str(c_id)
		arp.save()

	def getMonClasses(self):
		mon_classes=alertReport.objects.values('r_class').distinct()
		return mon_classes

class monitorItemsOps:
	def __init__(self):
		self.curl_timeout=5
		self.header="Meilishuo:uid:9789;ip:192.168.128.14"
		self.ardOps=alertRecordOps()
		self.arpOps=alertReportOps()
		self.am=alertMailAndMsg()
		self.cm=commonMethod()
		self.logger=self.cm.getLogger()
		self.pool=threadpool.ThreadPool(10)
		pass

	def getMonClasses(self):
		mon_classes=monitorItems.objects.values('m_class').distinct()
		return mon_classes

	def reportPassItem(self,name,info):
		"""

		:rtype: object
		"""
		name=u'%s' % name
		info=u'%s' % info
		monitor = Monitor(self.cm.report_token)
		monitor.add_pass(name,info)
		ret = monitor.report()
		#self.logger.info("%s report code: %s " % (name,ret["code"]))

	def reportFailItem(self,name,info):
		name=u'%s' % name
		info=u'%s' % info
		monitor = Monitor(self.cm.report_token)
		monitor.add_fail(name,info)
		ret = monitor.report()
		self.logger.info("%s fail, report code: %s " % (name,ret["code"]))

	def getTraceUsers(self,id):
		tracelist=self.am.getAllAlertUsers(id)
		if not tracelist:
			return ''
		traceusers=''
		for user in tracelist:
			traceusers+=','+user
		traceusers=traceusers.strip(',')
		return traceusers

	def getCurlCmd(self,mi):
		http_code="""%{http_code}"""
		if mi.m_class.lower() == 'data':
			if mi.m_params and mi.m_params.lower() != 'null':
				cmd="""curl --connect-timeout %s '%s?%s' -w %s """ % (self.curl_timeout,mi.m_url,mi.m_params,http_code)
			else:
				cmd="""curl --connect-timeout %s '%s' -w %s """ % (self.curl_timeout,mi.m_url,http_code)
			return cmd

		if not mi.m_host or mi.m_host.lower()=='null':
			cmd="""curl --connect-timeout %s --header '%s' '%s' -d '%s' -w %s """ % (self.curl_timeout,self.header,mi.m_url,mi.m_params,http_code)
		else:
			gz_url=mi.m_url
			if gz_url.__contains__('10.0.0.55'):
				gz_host=self.cm.getHostConf('10.0.0.55')
				gz_url=gz_url.replace('10.0.0.55',gz_host)
			if gz_url.__contains__('10.0.0.57'):
				gz_host=self.cm.getHostConf('10.0.0.57')
				gz_url=gz_url.replace('10.0.0.57',gz_host)
			cmd="""curl -H 'host:%s' --connect-timeout %s --header '%s' '%s' -d '%s' -w %s """ % (mi.m_host,self.curl_timeout,self.header,gz_url,mi.m_params,http_code)

		return cmd

	def runCmdAndCheckResult(self,cmd,mi):
		self.logger.info(cmd)
		reStr=os.popen(cmd).read()

		ckp=self.checkPrimaryResult(reStr,mi)
		if ckp:
			reStr=reStr[:-3]
			ckd=self.checkDetailResult(reStr,mi)
		else:
			ckd=False

		if ckp and ckd:
			arObj=self.ardOps.getRecordObject(mi.id)
			if arObj:
				duration=self.cm.calDuration(mi.id)
				duration=self.cm.formatTime(duration)
				traceusers=self.getTraceUsers(mi.id)
				self.arpOps.addAlertReport(mi.id,arObj.a_name,arObj.a_class,arObj.a_plat,arObj.a_city,arObj.a_createTime,arObj.a_alertTimes,duration,traceusers,arObj.a_errorType)
				self.ardOps.deleteRecord(mi.id)
			try:
				self.reportPassItem(mi.m_name,"pass")
			except Exception,e:
				#self.logger.exception(e)
				self.logger.info("%s report pass exception" % mi.id)

	def runAllMonitorItem(self):
		now=datetime.now()
		cur_min=now.minute
		monItems=monitorItems.objects.all()
		for mi in monItems:
			if mi.m_active.lower()=="false":
				continue
			if cur_min%mi.m_interval!=0:
				continue
			cmd=self.getCurlCmd(mi)
			try:
				requests=threadpool.makeRequests(self.runCmdAndCheckResult,[(None,{'cmd':cmd,'mi':mi})])
				[self.pool.putRequest(req) for req in requests]
				#self.runCmdAndCheckResult(cmd,mi)
				#thread.start_new_thread(self.runCmdAndCheckResult,(cmd,mi,))
			except Exception, e:
				self.logger.exception("%s => %s" % (mi.id,e))
		self.pool.wait()


	def optionsWhenError(self,mi,errorType):
		error_cmd=self.getCurlCmd(mi)
		self.logger.info("%s ====> %s" % (error_cmd,errorType))
		cur_time=self.cm.getFormatCurTime()
		if not self.ardOps.getRecordObject(mi.id):
			now = datetime.now()
			self.ardOps.addRecord(mi.id,mi.m_name,mi.m_class,mi.m_plat,mi.m_city,now,0,0,1,errorType)
		else:
			self.ardOps.updateAlertTimes(mi.id)
			self.ardOps.updateErrorType(mi.id,errorType)

		alertType=self.am.getAlertType(mi.id)

		if not alertType:
			pass
		else:
			duration = self.cm.calDuration(mi.id)
			duration = self.cm.formatTime(duration)
			mailSubj="%s 接口监控到异常" % (mi.m_name)
			msgContent="%s 接口监控到异常:%s发生时间:%s持续时间:%s" % (mi.m_url,errorType,cur_time,duration)
			sendStatus=self.am.sendAlert(mi.id,mi.m_alertUsers,msgContent,mailSubj,msgContent,alertType)
			try:
				self.reportFailItem(mi.m_name,msgContent)
			except Exception,e:
				#self.logger.exception(e)
				self.logger.info("%s report fail exception" % mi.id)
			if sendStatus:
				if alertType=='mail':
					self.ardOps.updateMailTimes(mi.id)
				if alertType=='msg':
					self.ardOps.updateMsgTimes(mi.id)

	def checkPrimaryResult(self,restr,mi):
		if not restr:
			return False
		reload(sys)
		sys.setdefaultencoding('utf-8')
		http_code=restr[-3:]
		if http_code != '200' :
			if http_code=='000':
				errorType="Request timeout"
			else:
				errorType="Http Status %s" % http_code
			self.optionsWhenError(mi,errorType)
			return False
		restr=restr[:-3]
		if restr.find(mi.m_expStr) < 0 :
			errorType="""doesn't match %s""" % (mi.m_expStr)
			self.optionsWhenError(mi,errorType)
			return False
		else:
			return True

	def checkDetailResult(self,restr,mi):
		if not restr:
			return False
		reload(sys)
		sys.setdefaultencoding('utf-8')
		if not mi.m_expDetailStr or mi.m_expDetailStr=='null':
			return True

		reStatus=True
		jStr=json.loads(mi.m_expDetailStr)
		paths=jStr['path'].split(",")
		expNums=jStr['expNum'].split(",")
		reJson=json.loads(restr)
		errorType="OK"
		for p in range(0,len(paths)):
			ckStrLen=self.cm.getValueOfPath(reJson,paths[p])
			if ckStrLen=="exception":
				errorType="%s 值为空" % paths
				self.optionsWhenError(mi,errorType)
				return False
			expNum=int(expNums[p])
			if(ckStrLen < expNum):
				reStatus = False
				self.logger.error("checkDetailResult error \n %s %s %s \n realLen: %s  expLen:%s" % (mi.m_url,mi.m_params, paths[p],ckStrLen, expNum))
				break

		if not reStatus:
			errorType="checkDetailResult error %s realLen: %s  expLen:%s" % (jStr['path'],ckStrLen, expNum)
			self.optionsWhenError(mi,errorType)

			return False
		else:
			return True



	# def updateComments(self,r_ID,comments):
	# 	pass
	#
	# def getAlertReportObj(self,r_ID):
	# 	try:
	#       arObj=alertReport.objects.get()



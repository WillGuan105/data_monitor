# -*-coding:utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.db.models import Q
from .models import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from difflib import *

import threading
import logging
import os
import json

getRunIds_lock=threading.Lock()
runJob_lock=threading.Lock()


header="Meilishuo:uid:9789;ip:192.168.128.14"
his_id=""
module=""
page=""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.

def getLogger():
	logger = logging.getLogger('smokeTest')
	FILE=os.path.join(BASE_DIR,'log')
	fh = logging.FileHandler(os.path.join(FILE,'smokeTest.log'))
	formatter = logging.Formatter('%(asctime)s -  %(filename)s[line:%(lineno)d]－%(name)s - %(levelname)s %(levelno)s : %(message)s')
	fh.setFormatter(formatter)
	logger.setLevel(logging.NOTSET)
	if logger.handlers:
		logger_len=len(logger.handlers)
		for i in range(0,logger_len):
			logger.handlers.pop(0)
	logger.addHandler(fh)
	return logger

logger=getLogger()

def smokeTest(request):
	global his_id,module,page
	his_id=request.GET.get('his_id')
	page=request.GET.get('page')
	module=request.GET.get('module')
	moduleObj=""
	if not page:
		page=1
	try:
		moduleObj=Modules.objects.get(m_name=str(module))
	except Exception,e:
		logger.exception(e)

	if moduleObj:
		intfs=Interface.objects.filter(i_module=moduleObj)
	else:
		intfs=Interface.objects.all()
	sepPageintf,totalPageIntfs=getPageContent(intfs,page)
	#reSet=set()
	tmpIds=getCurRunids()
	if tmpIds:
		qId=tmpIds[0]['his_id']
	else:
		return render_to_response('smokeTest.html',{'data':sepPageintf,"pages":totalPageIntfs,"module":module,"his_id":his_id})

	logger.info(qId)
	logger.info("******** %s" % str(his_id))
	if not his_id:
		his_id=qId
	for idx in range(0,len(sepPageintf)):
		#logger.info(type(sepPageintf[idx]))
		queryObj=runResult.objects.filter(Q(his_id=int(his_id)) & Q(intf=sepPageintf[idx]))
		logger.info(queryObj)
		if queryObj:
			sepPageintf[idx].i_status=str(queryObj[0].status)
		else:
			sepPageintf[idx].i_status="info"

		if len(sepPageintf[idx].i_params) >= 100:
			sepPageintf[idx].i_params=sepPageintf[idx].i_params[:90]+"..."
		#reSet.add(cur)

	return render_to_response('smokeTest.html',{'data':sepPageintf,'run_history':tmpIds,"pages":totalPageIntfs,"module":module,"his_id":his_id})

def querySmokeStatus(request):
	global his_id,module,page
	reDict={}
	his_id=request.GET.get('his_id')
	page=request.GET.get('page')
	module=request.GET.get('module')
	if not page:
		page=1
	smokeStatus=runResult.objects.filter(his_id=int(his_id))

	moduleObj=Modules.objects.get(m_name=module)

	intfs=Interface.objects.filter(i_module=moduleObj)
	for cur in intfs:
		cur_id=int(cur.i_ID)
		print "++++++++++++++ ",cur
		filter_status=smokeStatus.filter(intf=cur)
		if filter_status:
			cur_status=filter_status[0].status
			reDict[cur_id]=cur_status
		else:
			reDict[cur_id]="info"
	redata=(reDict)
	reJson=json.dumps(redata)
	return JsonResponse(reJson, safe=False)


def runSmokeTest(request):
	module=request.GET.get('module')
	his_id=getCurRunids()
	if len(his_id) > 0:
		his_id=his_id[0]['his_id']+1
	else:
		his_id=1

	online_host=request.GET.get('onlinehost')
	test_host=request.GET.get('testhost')
	runCommonTest(online_host,test_host,his_id,module)

	redict={"status":"done"}
	return JsonResponse(redict)


def runCommonTest(online_host,test_host,his_id,module):
	moduleObj=""
	try:
		moduleObj=Modules.objects.get(m_name=str(module))
	except Exception,e:
		logger.exception(e)

	if moduleObj:
		interfaces=Interface.objects.filter(i_module=moduleObj)
		logger.info("moduleObj is not null")
	else:
		interfaces=Interface.objects.all()
	
	for i in interfaces:
		try:
			online_log_file="/tmp/%s_online.txt" % (str(i.i_ID))
			test_log_file="/tmp/%s_test.txt" % (str(i.i_ID))
			runJob_lock.acquire()
			cleancmd="rm -f %s %s" % (online_log_file,test_log_file)
			os.system(cleancmd)
			online_cmd="%s > %s" % (getCurlCmd(online_host,i,module),online_log_file)
			test_cmd="%s > %s" % (getCurlCmd(test_host,i,module),test_log_file)
			logger.info("running cmd: \n ")
			logger.info(str(online_cmd))
			os.system(str(online_cmd))
			logger.info("running cmd: \n ")
			logger.info(str(test_cmd))
			os.system(str(test_cmd))
			diff_cmd="diff %s %s" % (online_log_file,test_log_file)
			ret=os.system(diff_cmd)
			if ret:
				job_re=runResult(his_id=his_id,intf=i,status="error",error_request=online_cmd)
				job_re.save()
				generateDetailDiff(online_log_file,test_log_file,his_id,i.i_ID)
			else:
				job_re=runResult(his_id=his_id,intf=i,status="success",error_request=online_cmd)
				job_re.save()
		except Exception, e:
			logger.exception(e)
		finally:
			runJob_lock.release()

def generateDetailDiff(online_file,test_file,his_id,job_id):

	try:
		diff_path="%s/static/smokeTestDiff" % BASE_DIR
		if not os.path.exists(diff_path):
			cmd="mkdir %s" % diff_path
			os.system(cmd)
		diff_file="%s/static/smokeTestDiff/%s_%s.html" % (BASE_DIR,his_id,job_id)
		cmd = 'touch %s' % (diff_file)
		os.system(cmd)
		if os.path.exists(diff_file):
			fp=open(diff_file,'w+')
			fromfile=open(online_file,'r').readlines()
			tofile=open(test_file,'r').readlines()
			diffhtml=HtmlDiff.make_file(HtmlDiff(),fromfile,tofile)
			diffhtml=('''%s''') % (diffhtml)
			diffhtml=diffhtml.replace('<head>','<head><meta charset="UTF-8">',1)
			diffhtml=diffhtml.replace('<td class="diff_next">','</tr><tr><td class="diff_next">',1)
			diffhtml=diffhtml.replace('nowrap="nowrap"','')
			diffhtml=diffhtml.replace('cellspacing="0" cellpadding="0" rules="groups"','border="1"')
			diffhtml=diffhtml.replace('1</td>','预期结果',1)
			diffhtml=diffhtml.replace('1</td>','实际结果',1)
			fp.write(diffhtml)
			fp.close()
	except Exception,e:
		logger.exception(e)



def getCurlCmd(host,interface,module):
	url="%s%s" % (host,interface.i_name)
	if module.lower() == "fakecube":
		cmd="""curl '%s?%s' """ % (url,interface.i_params)
	else:
		cmd="""curl --header '%s' %s -d '%s'  """ % (header,url,interface.i_params)
	return cmd


def getCurRunids():
	getRunIds_lock.acquire()
	try:
		ir=runResult.objects.values('his_id').distinct().order_by('his_id')
		ir=ir.reverse()[:10]
	finally:
		getRunIds_lock.release()
	return ir

def getPageContent(result_list,page):
	paginator=Paginator(result_list,10)
	try:
		result=paginator.page(page)
	except PageNotAnInteger:
		result=paginator.page(1)
	except EmptyPage:
		result=paginator.page(paginator.num_pages)

	return result,paginator


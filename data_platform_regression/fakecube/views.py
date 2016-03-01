#!coding: utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.context import RequestContext
from django.db.models import Q
import datetime
from django.views.decorators.csrf import csrf_exempt
from mysite.models import Report,Graph
from fakecube.models import FakecubeIF,FakecubeIFResult
import sys,os
sys.path.append('..')
from mysite.run import run
from frun import frun
import logging
import time
import os

from django.views.decorators.csrf import csrf_exempt
import json
import ast
import threading

getRunIds_lock=threading.Lock()
testlock = threading.Lock()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def helloworld(request):
    return HttpResponse("Hello world")

def cur_time(request):
	now = datetime.datetime.now()
	html = "<html><body> Now the time is %s" %now
	return HttpResponse(html)

def index(request):
	return render_to_response('index.html')

def queryFakecube(request):
	reSet=set()
	q=FakecubeIF.objects.all()
	rh=getCurRunfids()

	if not rh :
		return render_to_response('queryFakecube.html',{'data':q,'run_history':rh})

	queryId=rh[0]['fresult_id']
	for cur in q:
		t_gr=FakecubeIFResult.objects.filter(Q(fresult_id=int(queryId)) & Q(f_id=cur))
		if t_gr:
			cur.f_status=t_gr[0].f_status
		else:
			cur.f_status="info"
		reSet.add(cur)

	return render_to_response('queryFakecube.html',{'data':reSet,'run_history':rh})
	#p=FakecubeIF.objects.all()
	#return render_to_response('queryFakecube.html',{'data':p})

def queryFakecubeIFStatus(request):
	queryId=request.GET.get('queryId')
	reDict={}
	if not queryId:
		redata=(reDict)
		reJson=json.dumps(redata)
		return JsonResponse(reJson, safe=False)

	r_fakecube=FakecubeIFResult.objects.filter(fresult_id=int(queryId))
	
	q=FakecubeIF.objects.all()
	for cur in q:
		f_id=cur.f_id
		cur_status=r_fakecube.filter(f_id=cur).values('f_status')
		if cur_status:
			reDict[f_id]=str(cur_status[0]['f_status'])
		else:
			reDict[f_id]="info"
	redata=(reDict)
	reJson=json.dumps(redata)

	return JsonResponse(reJson, safe=False)

def getCurRunfids():
	lock=threading.Lock()
	lock.acquire()
	try:
		gr=FakecubeIFResult.objects.values('fresult_id').distinct().order_by('fresult_id')
		gr=gr.reverse()[:10]
	finally:
		lock.release()
	return gr


@csrf_exempt
def runfJob(request):
	logger=getLogger()

	#cleanDiffPath()
	f=FakecubeIF.objects.all()
	for tmp in f:
		tmp.f_status="info"
		tmp.save()
		print tmp.f_status

	cur_runfids=getCurRunfids()
	if not cur_runfids:
		fresult_id=1
	else:
		fresult_id=int(cur_runfids[0]['fresult_id'])+1 #以后需大数处理

	frunIds=request.GET.get('runJobIds')
	fidArr=frunIds.split(",")
	
	for i in fidArr:
		f=FakecubeIF.objects.get(f_id=int(i))
		fret=frun(fresult_id,i,f.frun_url)
		if(fret==0):
			f.f_status="success"
			logger.debug(str(i)+'success')
		else:
			f.f_status="error"
			logger.error(str(i)+'error')
		f.save()
		fr=FakecubeIFResult(fresult_id=fresult_id,f_id=f,f_status=f.f_status)
		fr.save()
		print f.f_id,f.f_status

	redict={"status":"done"}

	return JsonResponse(redict)


def getLogger():
	logger = logging.getLogger('fakecube')
	FILE=os.path.join(BASE_DIR,'log')
	fh = logging.FileHandler(os.path.join(FILE,'fakecube_view.log'))
	formatter = logging.Formatter('%(asctime)s -  %(filename)s[line:%(lineno)d]－%(name)s - %(levelname)s %(levelno)s : %(message)s')
	fh.setFormatter(formatter)
	logger.setLevel(logging.NOTSET)
	if logger.handlers:
		logger_len=len(logger.handlers)
		for i in range(0,logger_len):
			logger.handlers.pop(0)
	logger.addHandler(fh)
	return logger

def cleanDiffPath():
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	diff_files="%s/static/datadiff/*" % (BASE_DIR)
	cmd='rm -f ' + diff_files
	os.system(cmd)

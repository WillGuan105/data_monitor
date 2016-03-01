#!coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.context import RequestContext
from django.db.models import Q
import datetime
from models import Report,Graph,ReportResult,GraphResult
import sys,os
sys.path.append('..')
from run import run
from remote_ssh_cmd import *
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import threading
import logging
import time

getRunIds_lock=threading.Lock()
testlock = threading.Lock()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def hello(request):
	restr=""
	print "1",request.META['REMOTE_HOST']
	print "2",request.META['REMOTE_ADDR']
	print "3",request.META['HTTP_HOST']
	try:
		a=1/0
	except:
		restr=str(sys.exc_info())
		print restr
	# reqId = request.GET.get('reqId')
	# lk=testlock.acquire(False)
	# if lk :
	# 	print " id:%s is in lock %s ================ \n" % (reqId,lk)
	# 	time.sleep(10)
	# 	print " id:%s is after sleep ================ \n" % (reqId)
	# 	testlock.release()
	# 	restr= "Hello world %s =======" % (reqId)
	# else:
	# 	restr= "Hello is locked %s " % (reqId)
	return HttpResponse(restr)

def cur_time(request):
	now = datetime.datetime.now()
	html = "<html><body> Now the time is %s" %now
	return HttpResponse(html)

def index(request):
	return render_to_response('index.html')

def queryReport(request):
	reSet=set()
	q=Report.objects.all()
	rh=getCurRunrids()

	if not rh :
		return render_to_response('queryReport.html',{'data':q,'run_history':rh})

	queryId=rh[0]['result_id']
	for cur in q:
		t_gr=ReportResult.objects.filter(Q(result_id=int(queryId)) & Q(r_id=cur))
		if t_gr:
			cur.status=t_gr[0].status
		else:
			cur.status="info"
		reSet.add(cur)

	return render_to_response('queryReport.html',{'data':reSet,'run_history':rh})
	#q=Report.objects.all()
	#return render_to_response('queryReport.html',{'data':q})

def queryReportStatus(request):
	queryId=request.GET.get('queryId')
	reDict={}
	if not queryId:
		redata=(reDict)
		reJson=json.dumps(redata)
		return JsonResponse(reJson, safe=False)

	r_report=ReportResult.objects.filter(result_id=int(queryId))
	
	q=Report.objects.all()
	for cur in q:
		r_id=cur.r_id
		cur_status=r_report.filter(r_id=cur).values('status')
		if cur_status:
			reDict[r_id]=str(cur_status[0]['status'])
		else:
			reDict[r_id]="info"
	redata=(reDict)
	reJson=json.dumps(redata)
	return JsonResponse(reJson, safe=False)

def getCurRunrids():
	lock=threading.Lock()
	lock.acquire()
	try:
		gr=ReportResult.objects.values('result_id').distinct().order_by('result_id')
		gr=gr.reverse()[:10]
	finally:
		lock.release()
	return gr


def queryGraph(request):
	reSet=set()
	q=Graph.objects.all()
	rh=getCurRunids()

	if not rh :
		return render_to_response('queryGraph.html',{'data':q,'run_history':rh})

	queryId=rh[0]['result_id']
	for cur in q:
		t_gr=GraphResult.objects.filter(Q(result_id=int(queryId)) & Q(g_id=cur))
		if t_gr:
			cur.status=t_gr[0].status
		else:
			cur.status="info"
		reSet.add(cur)

	return render_to_response('queryGraph.html',{'data':reSet,'run_history':rh})

def queryGraphStatus(request):
	queryId=request.GET.get('queryId')
	reDict={}
	if not queryId:
		redata=(reDict)
		reJson=json.dumps(redata)
		return JsonResponse(reJson, safe=False)

	r_graph=GraphResult.objects.filter(result_id=int(queryId))
	
	q=Graph.objects.all()
	for cur in q:
		g_id=cur.g_id
		cur_status=r_graph.filter(g_id=cur).values('status')
		if cur_status:
			reDict[g_id]=str(cur_status[0]['status'])
		else:
			reDict[g_id]="info"
	redata=(reDict)
	reJson=json.dumps(redata)
	return JsonResponse(reJson, safe=False)

def getCurRunids():
	getRunIds_lock.acquire()
	try:
		gr=GraphResult.objects.values('result_id').distinct().order_by('result_id')
		gr=gr.reverse()[:10]
	finally:
		getRunIds_lock.release()
	return gr


@csrf_exempt
def graphDataDiff(request):
	logger=getLogger()
	
	g=Graph.objects.all()
	for tmp in g:
		tmp.status="info"
		tmp.save()
		print tmp.status
	cur_runids=getCurRunids()
	if not cur_runids :
		result_id=1
	else:
		result_id=int(cur_runids[0]['result_id'])+1   #未来需要大数处理

	runIds=request.GET.get('runJobIds')
	idArr=runIds.split(",")
	
	for i in idArr:
		g=Graph.objects.get(g_id=int(i))
		ret=run(result_id,i,g.run_url)
		if(ret==0):
			g.status="success"
			logger.debug(str(i)+' success')
		else:
			g.status="error"
			logger.error(str(i)+' error')
		g.save()
		gr=GraphResult(result_id=result_id,g_id=g,status=g.status)
		gr.save()
		print g.g_id,g.status
		
	redict={"status":"done"}

	return JsonResponse(redict)

@csrf_exempt
def reportPicDiff(request):	
	logger=getLogger()

	#cleanPicDiffPath()
	r=Report.objects.all()
	for tmp in r:
		tmp.status="info"
		tmp.save()
		print tmp.status

	cur_runids=getCurRunrids()
	if not cur_runids :
		result_id=1
	else:
		result_id=int(cur_runids[0]['result_id'])+1   #未来需要大数处理
	
	runIds=request.GET.get('runJobIds')
	idArr=runIds.split(",")

	ret=getPicCom()
	data_string=ret[0]
	data_string=ast.literal_eval(data_string)

	foundDiff=False
	for i in idArr:
		if (i=="1067"):
			continue
		r=Report.objects.get(r_id=int(i))
		if(data_string[i]==1):
			r.status="success"
			print "same"
		else:
			foundDiff=True
			r.status="error"
			logger.error(str(i) + 'not same')
			print "not same"
		r.save()
		gr=ReportResult(result_id=result_id,r_id=r,status=r.status)
		gr.save()
		print r.r_id,r.status

	if foundDiff:
			scpPics(str(result_id))

	redict={"status":"done"}
	return JsonResponse(redict)

@csrf_exempt
def replaceStand(request):
	logger=getLogger()
	runIds=request.GET.get('repIds')
	idArr=runIds.split(",")

	repstatus=True
	for i in idArr:
		cmd="cp -f %s/mysite/result/%s.txt %s/mysite/stand/" % (BASE_DIR,str(i),BASE_DIR)
		logger.info("excecuting cmd ...... \n %s" % (cmd))
		ret=os.system(cmd)
		if ret:
			repstatus=False

	if repstatus:
		redict={"status":"success"}
	else:
		redict={"status":"fail"}

	return JsonResponse(redict)


def getLogger():
	logger = logging.getLogger('mysite')
	FILE=os.path.join(BASE_DIR,'log')
	fh = logging.FileHandler(os.path.join(FILE,'mysite_view.log'))
	formatter = logging.Formatter('%(asctime)s -  %(filename)s[line:%(lineno)d]－%(name)s - %(levelname)s %(levelno)s : %(message)s')
	fh.setFormatter(formatter)
	logger.setLevel(logging.NOTSET)
	if logger.handlers:
		logger_len=len(logger.handlers)
		for i in range(0,logger_len):
			logger.handlers.pop(0)
	logger.addHandler(fh)
	return logger

def getPicCom():
	result=getPicComResult()	
	return result

def cleanDiffPath():
	diff_files="%s/static/datadiff/*" % (BASE_DIR)
	cmd='rm -f ' + diff_files
	os.system(cmd)

def cleanPicDiffPath():
	diff_path="%s/static/diffPNG/*" % (BASE_DIR)
	cmd='rm -f ' + diff_path
	os.system(cmd)




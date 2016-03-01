# -*-coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sendmail import sendMail
from PayAutoTest.models import PayResult
import os,sys,re,string,time
import logging
import threading
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#paytest_path = '/home/work/dataplatform'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paytest_path = '%s/..' % (BASE_DIR)
pay_lock = threading.Lock()


def getLogger():
    logger = logging.getLogger()
    FILE = os.path.join(BASE_DIR, 'log')
    fh = logging.FileHandler(os.path.join(FILE, 'payautotest.log'))
    formatter = logging.Formatter('%(asctime)s -  %(filename)s[line:%(lineno)d]－%(name)s - %(levelname)s %(levelno)s: %(message)s')
    fh.setFormatter(formatter)
    logger.setLevel(logging.NOTSET)
    if logger.handlers:
        logger_len=len(logger.handlers)
        for i in range(0,logger_len):
            logger.handlers.pop(0)
    logger.addHandler(fh)
    return logger

logger=getLogger()

def payautotest(request):
    return render_to_response('PayAutoTest.html')


def payautotestnew(request):
    return render_to_response('PayAutoTestNew.html')

def gettime():
    return time.strftime('%Y-%m-%d %X',time.localtime())


def showresult(request):
	f=open('log/payautotest.log',"r")
	try:
		rtext=f.readlines()
	finally:
		f.close
	return render_to_response('showresult.html',{'data':rtext})


@csrf_exempt
def runpaytest(request):
    #先清空日志文件
    f=open('log/payautotest.log',"w")
    try:
        f.truncate(0)
    finally:
        f.close()

    remote_http = request.META['HTTP_HOST']
    mailto = request.GET.get('mail')
    user = mailto.split('@')[0]
    jobid = request.GET.get('jobid').strip()
    runtype=request.GET.get('runtype').strip()
    #result_link = "/static/paytestresult/%s_paytestresult/%s/surefire-reports/index.html" % (user, jobid)
    result_link="/static/paytestresult/%s_paytestresult/%s/result.html" % (user,jobid)
    try:
        logger.info("runpaytest is called ......")
        file_path = '%s/%s_PayAutoTest' % (paytest_path, user)
        logger.info(file_path)
        if runtype =='newpay':
            file_path='%s/%s_PayAutoTestNew' % (paytest_path,user)
    	if runtype=='smoke':
    	    file_path='%s/%s_PayAutoTestSmoke' % (paytest_path,user)
        if not os.path.exists(file_path):
            cmd = 'mkdir %s' % (file_path)
            os.system(cmd)
        else:
	        cmd='cd %s;rm -rf *' % (file_path)
	        os.system(cmd)
        if runtype =='newpay':
		    cmd="cd %s; svn co http://svn.meilishuo.com/repos/qa/PayAutoTestNew/ %s" % (paytest_path,file_path)
		    re=os.popen(cmd).read()
        if runtype=='smoke':
            cmd="cd %s; svn co http://svn.meilishuo.com/repos/qa/PaySmokeTest/ %s" % (paytest_path,file_path)
            re=os.popen(cmd).read()
        else:
        	cmd = "cd %s; svn co http://svn.meilishuo.com/repos/qa/PayAutoTest/ %s" % (paytest_path, file_path)
        	re = os.popen(cmd).read()
        logger.info("checkout svn code......")

        dbconf = request.GET.get('dbconf')
        conf = request.GET.get('config')
        #任务id,创建文件夹保存结果
        #jobid=request.GET.get('jobid').strip()
        user_result="%s/static/paytestresult/%s_paytestresult" % (BASE_DIR,user)

        if not os.path.exists(user_result):
            cmd="cd %s/static/paytestresult/;mkdir %s_paytestresult" % (BASE_DIR,user)
            re=os.popen(cmd).read()
        cmd = "cd %s/static/paytestresult/%s_paytestresult;mkdir %s" % (BASE_DIR, user, jobid)
        re = os.popen(cmd).read()
        logger.info("make resultfile dir......")

        env=str(conf).split('username')[0].split('labn=')[1]
        logger.info("executed env:%s" % (env))

        cmd = 'cd %s/src/main/resources/; echo "%s" > ./interface.properties; echo "%s" > ./db.properties' % (file_path, str(conf), str(dbconf))
        re = os.popen(cmd).read()

        logger.info("executed cmd:mvn clean install......")
        cmd = "cd %s; mvn clean install" % (file_path)
        ctime=gettime()
        re = os.popen(cmd).read()
        logger.info("executed result: \n %s" % (re))

        cmd = 'cd %s/target/surefire-reports; cat testng-results.xml | grep "<testng-results"' % (file_path)
        re = os.popen(cmd).read()
        test_result = re

        cmd = 'cp -rf %s/result.html %s/static/paytestresult/%s_paytestresult/%s' % (file_path, BASE_DIR, user, jobid)
        re = os.popen(cmd).read()

        #结果链接保存到数据库
        etime=gettime()
        caselink = "/static/paytestresult/%s_paytestresult/%s/result.html" % (user, jobid)
        pr = PayResult(jobid=jobid, result=caselink, author=user,env=env,ctime=ctime,etime=etime)
        pr.save()
    except:
        test_result = str(sys.exc_info())
    mail_result_link = "%s%s" % (remote_http, result_link)
    mail_content = getContent(test_result, mail_result_link, dbconf, conf)
    subj = "%s PayAutoTest run result" % (user)
    sendMail([mailto], subj, mail_content)
    redict = {"status": test_result, "r_link": result_link}
    return JsonResponse(redict)


@csrf_exempt
def runpaytestnew(request):
    remote_http = request.META['HTTP_HOST']
    mailto = request.GET.get('mail')
    user = mailto.split('@')[0]
    jobid = request.GET.get('jobid').strip()
    result_link = "/static/paytestresult/%s_paytestresult/%s/surefire-reports/index.html" % (user, jobid)
    try:
        logger.info("runpaytest is called ......")
        file_path = '%s/%s_PayAutoTestNew' % (paytest_path, user)
        logger.info("file_path: %s" % (file_path))
        if os.path.exists(file_path):
            cmd = 'rm -rf %s' % (file_path)
            os.system(cmd)

        cmd = "cd %s; svn co http://svn.meilishuo.com/repos/qa/PayAutoTestNew/ %s" % (paytest_path, file_path)
        re = os.popen(cmd).read()
        logger.info("executed cmd: \n %s" % (cmd))
        logger.info("executed result: \n %s" % (re))

        dbconf = request.GET.get('dbconf')
        conf = request.GET.get('config')
        #任务id,创建文件夹保存结果
        #jobid=request.GET.get('jobid').strip()
        cmd = "cd %s/static/paytestresult/%s_paytestresult;mkdir %s" % (BASE_DIR, user, jobid)
        re = os.popen(cmd).read()
        logger.info("executed cmd: \n %s" % (cmd))
        logger.info("executed result: \n %s" % (re))

        cmd = 'cd %s/src/main/resources/; echo "%s" > ./interface.properties; echo "%s" > ./db.properties' % (
        file_path, str(conf), str(dbconf))
        re = os.popen(cmd).read()
        logger.info("executed cmd: \n %s" % (cmd))
        logger.info("executed result: \n %s" % (re))

        cmd = "cd %s; mvn clean install" % (file_path)
        re = os.popen(cmd).read()
        logger.info("executed cmd: \n %s" % (cmd))
        logger.info("executed result: \n %s" % (re))

        cmd = 'cd %s/target/surefire-reports; cat testng-results.xml | grep "<testng-results"' % (file_path)
        re = os.popen(cmd).read()
        test_result = re
        logger.info("executed cmd: \n %s" % (cmd))
        logger.info("executed result: \n %s" % (re))

        cmd = 'cp -rf %s/target/surefire-reports %s/static/paytestresult/%s_paytestresult/%s' % (file_path, BASE_DIR, user, jobid)
        re = os.popen(cmd).read()
        logger.info("executed cmd: \n %s" % (cmd))
        logger.info("executed result: \n %s" % (re))

        #结果链接保存到数据库
        caselink = "/static/paytestresult/%s_paytestresult/%s/surefire-reports/index.html" % (user, jobid)
        pr = PayResult(jobid=jobid, result=caselink, author=user)
        pr.save()

    except Exception, e:
        logger.exception(e)
    mail_result_link = "%s%s" % (remote_http, result_link)
    mail_content = getContent(test_result, mail_result_link, dbconf, conf)
    subj = "%s PayAutoTest run result" % (user)
    sendMail([user], subj, mail_content)
    redict = {"status": test_result, "r_link": result_link}
    return JsonResponse(redict)


# def getContent(result, link, dbconf, conf):
#     mail_content = """
# 	run result: \n
# 	%s \n
# 	result link: \n
# 	%s \n
# 	dbconf: \n
# 	%s \n
# 	Case conf: \n
# 	%s \n
# 	""" % (result, link, dbconf, conf)
#     print mail_content
#     return mail_content

def getContent(result,link,dbconf,conf):
    match=re.search(r'skipped="(\w+)" failed="(\w+)" total="(\w+)" passed="(\w+)"',result)
    result=match.group(0)
    match=re.search(r'DB_DataBase=(\w+)',dbconf)
    dbconf=match.group(0)
    mail_content="""
			<html>
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>PayAutoTest Result</title>
            </head>
            <body>
            <H1>PayAutoTest Result</h1>
            <table>
            <tr><td>Result</td><td>%s</td></tr>
            <tr><td>Link</td><td><a href="http://%s">%s</a></td></tr>
            <tr><td>dbconf</td><td>%s</td></tr>
            <tr><td>caseconf</td><td>%s</td></tr>
            </table>
                        </body>
                        </html>
                        """ % (result,link,link,dbconf,conf)
    return mail_content


def payresult(request):
    #result_list=PayResult.objects.all()
    result_list=PayResult.objects.order_by('-id').all()
    paginator=Paginator(result_list,10)
    page=request.GET.get('page')
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)

    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            result_list = PayResult.objects.filter(jobid__icontains=q).order_by('-id')
            paginator=Paginator(result_list,10)
            try:
                result=paginator.page(page)
            except PageNotAnInteger:
                result=paginator.page(1)
            except EmptyPage:
                result=paginator.page(paginator.num_pages)
            return render_to_response('payresult.html',{'data': result})

    if 'r' in request.GET:
        r = request.GET['r']
        if r:
            result_list = PayResult.objects.filter(author__icontains=r).order_by('-id')
            paginator=Paginator(result_list,10)
            try:
                result=paginator.page(page)
            except PageNotAnInteger:
                result=paginator.page(1)
            except EmptyPage:
                result=paginator.page(paginator.num_pages)
            return render_to_response('payresult.html',{'data': result})

    return render_to_response('payresult.html',{'data': result})

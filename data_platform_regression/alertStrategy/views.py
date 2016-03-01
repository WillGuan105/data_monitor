# -*-coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .alertController import *
from .sendmail import *
import os,sys
from django.core.paginator import *
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
import operator

header="Meilishuo:uid:9789;ip:192.168.128.14"
systemAlertUsers=['weiguan']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file="%s/alertStrategy/conf/domain_conf.ini" % (BASE_DIR)
data_file="%s/static/data/mData.txt" % (BASE_DIR)
cm=commonMethod()
am = alertMailAndMsg()
ardOps=alertRecordOps()
arpOps=alertReportOps()
miOps=monitorItemsOps()
logger = cm.getLogger()

def getMonitorCurlCmd(request):
    rstr=''
    mid = request.GET.get('mid')
    mi=getObject(mid)
    if not mi:
        rstr+='No moniter name id is %s'%mid
        return HttpResponse(rstr)
    cmd = miOps.getCurlCmd(mi)
    rstr+=cmd
    return HttpResponse(rstr)

def getObject(cname):
    try:
        ar= monitorItems.objects.get(id=cname)
        return ar
    except ObjectDoesNotExist:
        return None

def queryAlert(request):
    m_class=request.GET.get('mClass')
    if not m_class or m_class.lower() == 'all':
        q=monitorItems.objects.all()
    else:
        q=monitorItems.objects.filter(m_class=m_class)
    #q=monitorItems.objects.order_by('m_status')
    al=alertRecord.objects.all()
    sucnum=0
    errnum=0
    warnnum=0
    aid = set()
    #status = []
    status = {}

    if not q:
        return HttpResponse('There is no Monitor Items!')

    for a in al:
        aid.add(a.a_ID)

    for m in q:
        item = []
        item.append(m.id)
        mix_name="%s(%s)" % (m.m_name,m.m_url.split('/')[-1].split('?')[0])
        item.append(mix_name)
        item.append(m.m_class)
        if m.m_active == 'False':
            item.append('not useful')
            warnnum = warnnum+1
        elif m.id in aid:
            item.append('error')
            errnum = errnum+1
        else:
            item.append('success')
            sucnum = sucnum+1
        #status.append(item)
        status[m.id] = item

    sortstatus= sorted(status.items(), key=lambda x:x[1][3])
    #sortstatus= sorted(status, key=lambda x:x[3])

    page=request.GET.get('page')
    if not page:
		page=1
    sepPageintf,totalPageIntfs=getPageContent(sortstatus,page)
    print 'sepPageintf is %s ***********************'%type(sepPageintf)

    mon_classes=miOps.getMonClasses()
    tmp={'m_class':'all'}
    mon_classes=list(mon_classes)
    mon_classes.insert(0,tmp)

    return render_to_response('listmonitor.html',{'data':sepPageintf,"pages":totalPageIntfs,'sucnum':sucnum,'errnum':errnum,'warnnum':warnnum,'mon_classes':mon_classes,'m_class':m_class})

def getPageContent(result_list,page):
	limit =10
	paginator=Paginator(result_list,limit)
	try:
		result=paginator.page(page)
	except PageNotAnInteger:
		result=paginator.page(1)
	except EmptyPage:
		result=paginator.page(paginator.num_pages)

	return result,paginator

def getAllMonitorReport(request):
    #b_class=request.GET.get('belongClass')
    #begin=request.GET.get('begin')
    #end=request.GET.get('end')
    alert_reports=None
    classDict={}
    interfDict={}
    #alert_records=None
    alert_records=ardOps.getRecordItems()
    '''
    if b_class and begin and end:
        begin="%s 00:00:00" % begin
        begin=str_to_datetime(begin)
        end="%s 23:59:59" % end
        end=str_to_datetime(end)
        alert_reports=arpOps.getAlertReport(b_class,begin,end)
        alert_records=ardOps.getRecordItems()
    '''

    if alert_reports:
        alert_reports,classDict,interfDict,alert_records=dealAndStatistic(alert_reports,alert_records)

    mon_classes=arpOps.getMonClasses()
    tmp={'r_class':'all'}
    mon_classes=list(mon_classes)
    mon_classes.insert(0,tmp)

    return render_to_response('listmonitor.html',{'alertReports':alert_reports,'mon_classes':mon_classes,'classDict':classDict,'interfDict':interfDict,'alert_records':alert_records})


def loadData(request):
    dFile=open(data_file)
    line=dFile.readline()
    while line.strip():
        line=line.strip('\n')
        lArr=line.split("|")
        line=dFile.readline()
        mi=monitorItems(id=lArr[0],m_active=lArr[1],m_name=lArr[2],m_class=lArr[3],m_url=lArr[4],m_params=lArr[5],m_host=lArr[6],m_plat=lArr[7],m_city=lArr[8],m_expStr=lArr[9],m_expDetailStr=lArr[10],m_alertUsers=lArr[11],m_interval=lArr[12])
        mi.save()
    dFile.close()
    return HttpResponse("suc")

def str_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%d %X")

def updateComments(request):
    status="fail"
    rpid=request.GET.get('rpid')
    comments=request.GET.get('comments')
    if rpid and comments:
        arpOps.updateComments(rpid,comments)
        status="suc"
    return HttpResponse(status)


def getAlertReport(request):
    b_class=request.GET.get('belongClass')
    begin=request.GET.get('begin')
    end=request.GET.get('end')
    alert_reports=None
    classDict={}
    interfDict={}
    alert_records=None

    if b_class and begin and end:
        begin="%s 00:00:00" % begin
        begin=str_to_datetime(begin)
        end="%s 23:59:59" % end
        end=str_to_datetime(end)
        alert_reports=arpOps.getAlertReport(b_class,begin,end)
        alert_records=ardOps.getRecordItems()

    print alert_reports
    print "************&&&&&&&&&&&&&&&&&&&&"

    if alert_reports or alert_records:
        print "enterin"
        alert_reports,classDict,interfDict,alert_records=dealAndStatistic(alert_reports,alert_records)


    print alert_reports
    print type(alert_reports)
    print "************&&&&&&&&&&&&&&&&&&&&"
    midaplist=None
    i=0
    if alert_reports:
        midaplist=[]
        for ap in alert_reports:
            alist=[]
            namelist=ap.r_interfaceName.split('/')
            if len(namelist) <=1:
                mid =None
            else:
                mid = namelist[-1]
            #mid= ap.r_interfaceName.split('/')[-1]
            alist.append(mid)
            apargs=[]
            apargs.append(ap.r_interfaceName)
            apargs.append(ap.r_class)
            apargs.append(ap.r_plat)
            apargs.append(ap.r_city)
            apargs.append(ap.r_createTime)
            apargs.append(ap.r_duration)
            apargs.append(ap.r_alertTimes)
            apargs.append(ap.r_traceUsers)
            apargs.append(ap.r_comments)
            '''
            print apargs
            print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            print ap
            print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
           '''
            alist.append(apargs)
            alist.append(ap.id)
            midaplist.append(alist)
            #print mid

    mon_classes=arpOps.getMonClasses()
    tmp={'r_class':'all'}
    mon_classes=list(mon_classes)
    mon_classes.insert(0,tmp)

    return render_to_response('alertReport.html',{'midaplist':midaplist,'alertReports':alert_reports,'mon_classes':mon_classes,'classDict':classDict,'interfDict':interfDict,'alert_records':alert_records})

def runAllMonitor(request):
    miOps.runAllMonitorItem()
    return HttpResponse('alldone')

def sendMailService(request):
    reload(sys)
    sys.setdefaultencoding('utf8')
    to=request.GET.get('to')
    to=to.split(",")
    b_class=request.GET.get('belongClass')
    begin=request.GET.get('begin')
    end=request.GET.get('end')

    alert_reports=None
    classDict={}
    interfDict={}
    alert_records=None
    if b_class and begin and end:
        begin="%s 00:00:00" % begin
        begin=str_to_datetime(begin)
        end="%s 23:59:59" % end
        end=str_to_datetime(end)
        alert_reports=arpOps.getAlertReport(b_class,begin,end)
        alert_records=ardOps.getRecordItems()

    if alert_reports:
        alert_reports,classDict,interfDict,alert_records=dealAndStatistic(alert_reports,alert_records)

    mailSubj="""%s ~ %s %s 监控报表""" % (begin,end,b_class)
    mailContent="""%s""" % str(render_to_response('mailTemplate.html',{'alertReports':alert_reports,'classDict':classDict,'interfDict':interfDict,'alert_records':alert_records}))

    mailSt=sendMail(to,mailSubj,mailContent)
    if mailSt:
        return HttpResponse("邮件发送成功")
    else:
        return HttpResponse("邮件发送失败！！！")

def dealAndStatistic(alert_reports, alert_records):
    # if not alert_reports:
    #     return None
    alert_reports=set(alert_reports)
    classDict={}
    interfDict={}
    re_alert_records=set()

    for ad in alert_records:
        alertUsers=miOps.getTraceUsers(ad.a_ID)
        dur=cm.calDuration(ad.a_ID)
        dur=cm.formatTime(dur)
        crtime = ad.a_createTime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
        crtime = crtime.replace(tzinfo=None)
        crtime = crtime.__format__('%Y-%m-%d %X')
        tmp=alertReport(id=ad.a_ID,r_interfaceName=ad.a_name,r_class=ad.a_class,r_plat=ad.a_plat,r_city=ad.a_city,r_createTime=crtime,r_alertTimes=ad.a_alertTimes,r_duration=dur,r_traceUsers=alertUsers,r_comments=ad.a_errorType+ " 尚未修复")
        re_alert_records.add(tmp)

    for ar in alert_reports:
        crtime = ar.r_createTime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
        crtime = crtime.replace(tzinfo=None)
        tmp=ar
        tmp.r_createTime=crtime.__format__('%Y-%m-%d %X')
        users=tmp.r_traceUsers.split(",")
        if len(users) > 2:
            tmp.r_traceUsers=users[0]+","+users[1]+",..."
        alert_reports.remove(ar)
        alert_reports.add(tmp)

        if classDict.__contains__(ar.r_class):
            classDict[ar.r_class]=classDict[ar.r_class]+ar.r_alertTimes
        else:
            classDict[ar.r_class]=ar.r_alertTimes

        if interfDict.__contains__(ar.r_interfaceName):
            interfDict[ar.r_interfaceName]=interfDict[ar.r_interfaceName]+ar.r_alertTimes
        else:
            interfDict[ar.r_interfaceName]=ar.r_alertTimes
    alert_reports=sorted(alert_reports,key=operator.attrgetter('r_createTime'),reverse=True)
    classDict=sorted(classDict.items(),key=lambda c:c[1],reverse=True)
    interfDict=sorted(interfDict.iteritems(),key=lambda i:i[1],reverse=True)
    re_alert_records=sorted(re_alert_records,key=operator.attrgetter('r_createTime'),reverse=True)
    return alert_reports,classDict,interfDict,re_alert_records



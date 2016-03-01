# coding:utf-8
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import sys 
 

reload(sys)
sys.setdefaultencoding('utf-8')

def naccounttools(request):
    return render_to_response('naccounttools.html')

@csrf_exempt
def fenbiao(request):
     
    type = request.GET.get('usertype')
    name = request.GET.get('username')
    cmd = 'java -jar ./naccounttools/accountfenbiao.jar'+' '+type+' '+name
    os.system(cmd)
    f=open("result.txt",'r')
    content=f.readline()
    redict = {"status": content }

    return JsonResponse(redict)



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@csrf_exempt
def checkAccount(request):
    #获取参数
    payTypeValue = request.GET.get('payType')
    payIdValue=request.GET.get('payId')
    walletAmountValue=request.GET.get('walletAmount')
    if walletAmountValue=='':
        walletAmountValue='0'
    payAmountValue=request.GET.get('payAmount')
    if payAmountValue=='':
        payAmountValue='0'
    couponAmountValue=request.GET.get('couponAmount')
    if couponAmountValue=='':
        couponAmountValue='0'
    iouAmountValue=request.GET.get('iouAmount')
    if iouAmountValue=='':
        iouAmountValue='0'
    activityTypeValue=request.GET.get('activityType')
    activityAmountValue=request.GET.get('activityAmount')
    if activityAmountValue=='':
        activityAmountValue='0'
    handleTypeValue=request.GET.get('handleType')
    handleAmountValue=request.GET.get('handleAmount')
    if handleAmountValue=='':
        handleAmountValue='0'
    refundTypeValue=request.GET.get('refundType')
    conf='payId='+payIdValue+'\npayType='+payTypeValue+'\nwalletAmount='+walletAmountValue+'\npayAmount='+payAmountValue+'\ncouponAmount='+couponAmountValue+'\niouAmount='+iouAmountValue+'\nactivityType='+activityTypeValue+'\nactivityAmount='+activityAmountValue+'\nhandleType='+handleTypeValue+'\nhandleAmount='+handleAmountValue+'\nrefundType='+refundTypeValue+'\n'

    #从svn下载代码
    paytest_path ='%s/..' % (BASE_DIR)
    file_path='%s/CheckAccount' % (paytest_path)
    cmd="cd %s; svn co http://svn.meilishuo.com/repos/qa/CheckAccount/ %s" % (paytest_path,file_path)
    re=os.popen(cmd).read()
    #结果文件保留地址
    result="%s/static/accountresult" % (BASE_DIR)
    #写入配置文件
    cmd = 'cd %s/src/main/resources/; echo "%s" > ./case.properties' % (
        file_path, str(conf))
    re = os.popen(cmd).read()
    #执行mvn工程
    cmd = "cd %s; mvn clean install" % (file_path)
    re = os.popen(cmd).read()
    #获取结果文件
    cmd = 'cp -rf %s/result.txt %s/static/accountresult' % (file_path, BASE_DIR)
    re = os.popen(cmd).read()

    resultFile="%s/static/accountresult/result.txt" % (BASE_DIR)
    f=open(resultFile,'r')
    content=f.readlines()
    redict = {"result": content }
    return JsonResponse(redict)

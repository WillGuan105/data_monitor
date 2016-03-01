# -*-coding:utf-8 -*-
from django.shortcuts import render_to_response
from connectdb import db_connect,db_op
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import PropertiesParser
import os,os.path


diffile_path = '/home/work/dataplatform/diffile'


def paytools(request):
    return render_to_response('paytools.html')

@csrf_exempt
def clearwallet(request):
    userid = request.GET.get('userid')
    #清除实名认证
    clearrealname_data(userid)
    #清除钱包信息
    clearwallet_data(userid)
    redict = {"status": "customer_account;customer_info;accountinfo;t_dolphin_user_security_info"}
    return JsonResponse(redict)




@csrf_exempt
def clearrealname(request):
    userid = request.GET.get('userid')
    clearrealname_data(userid)
    redict = {"status": "realname_auth;realname_record;pay_cardinfo;pay_boundcardinfo;encrypt_data_card"}
    return JsonResponse(redict)


@csrf_exempt
def clearsecstore(request):
    userid = request.GET.get('userid')
    cardholder=request.GET.get('cardholder')
    clearsecStore_data(userid,cardholder)
    redict = {"status": "pay_boundcardinfo;pay_cardinfo;realname_auth;encrypt_data_card"}
    return JsonResponse(redict)


@csrf_exempt
def diffile(request):
    fileA = request.GET.get('fileA')
    fileB=request.GET.get('fileB')
    #获取文件名
    p,f1=os.path.split(fileA)
    print f1

    cmd="cd %s; svn cat %s > %s" % (diffile_path,fileA,f1)
    re=os.popen(cmd).read()
    print cmd

    #获取文件名
    p,f2=os.path.split(fileB)
    print f2
    if(f1==f2):
	    f2="testbak.properties"
    cmd="cd %s; svn cat %s > %s" % (diffile_path,fileB,f2)
    print cmd
    re=os.popen(cmd).read()


    p1=PropertiesParser.Properties()
    p2=PropertiesParser.Properties()
    p1.load(open('%s/%s' % (diffile_path,f1)))
    p2.load(open('%s/%s' % (diffile_path,f2)))
    a=p1.propertyNames()
    b=p2.propertyNames()
    #b中有a中没有的
    difA=list(set(b).difference(set(a)))
    #a中有b中没有的
    difB=list(set(a).difference(set(b)))
    redict = {"status": "文件A有B没有的:%s,文件B有A没有的:%s" % (difB,difA) }
    return JsonResponse(redict)




def clearrealname_data(userid):
    host = "10.8.3.40"
    port = "3323"
    user = "mlstmpdb"
    pwd = "yourpwd"
    dbname = "pay_member_center"
    db = db_connect(host,port,user,pwd,dbname)

    host2 = "10.8.3.36"
    port2 = "3342"
    user2 = "mlstmpdb"
    pwd2 = "yourpwd"
    dbname2= "pay_pay"
    db2 = db_connect(host2,port2,user2,pwd2,dbname2)


    sql1="delete from securestore.encrypt_data_card where encrypt_index in(select securityIndex from pay_member_center.realname_auth where custNo='%s')" %(userid)
    db_op(sql1, db)

    sql6="delete from securestore.encrypt_data_card where encrypt_index in(select securityIndex from pay_member_center.realname_record where userId='%s')" %(userid)
    db_op(sql6, db)

    sql2="delete from realname_auth  where custNo='%s'" % (userid)
    db_op(sql2, db)
    sql3="delete from pay_cardinfo where id in (select cardinfoId from pay_boundcardinfo where userId='%s')"  % (userid)
    db_op(sql3,db2)
    sql4="delete from pay_boundcardinfo where userId='%s'" % (userid)
    db_op(sql4,db2)
    sql5="delete from realname_record  where userId='%s'" % (userid)
    db_op(sql5,db)
    # disconnect from server
    db.close()


def clearwallet_data(userid):
    host = "10.8.3.40"
    port = "3323"
    user = "mlstmpdb"
    pwd = "yourpwd"
    dbname = "pay_member_center"
    db = db_connect(host,port,user,pwd,dbname)

    #clear dolphin message
    host2 = "10.6.7.49"
    port2 = "3306"
    user2 = "mlstmpdb"
    pwd2 = "yourpwd"
    dbname2 = "dugong"
    db2 = db_connect(host2,port2,user2,pwd2,dbname2)

    sql1="delete from customer_account where  user_id='%s'" % (userid)
    db_op(sql1, db)
    sql2="delete from customer_info where user_id='%s'" % (userid)
    db_op(sql2, db)

    sql4="delete from mlspay_account.accountinfo where custNo='%s'" % (userid)
    db_op(sql4, db)
    db.close()

    sql3="delete from  t_dolphin_user_security_info  where user_id='%s'" % (userid)
    db_op(sql3, db2)
    db2.close()

def clearsecStore_data(userid,cardholder):
    host = "10.8.3.40"
    port = "3323"
    user = "mlstmpdb"
    pwd = "yourpwd"
    dbname = "pay_member_center"
    db = db_connect(host,port,user,pwd,dbname)


    host2 = "10.8.3.36"
    port2 = "3342"
    user2 = "mlstmpdb"
    pwd2 = "yourpwd"
    dbname2= "pay_pay"
    db2 = db_connect(host2,port2,user2,pwd2,dbname2)


    sql1="delete from pay_boundcardinfo where cardinfoid in (select id from pay_cardinfo where cardHolder ='%s') and userid='%s'" % (cardholder,userid)
    db_op(sql1, db2)

    sql5="select secureindex from pay_cardinfo where cardHolder='%s')" % (cardholder)
    rows=db_op(sql5,db2)

    sql2="delete from securestore.encrypt_data_card where encrypt_index in %s" % (rows)
    db_op(sql2, db)
    sql3="delete from pay_cardinfo where cardHolder ='%s'" % (cardholder)
    db_op(sql3, db2)
    sql4="delete from realname_auth where name='%s' and custNo='%s'" % (cardholder,userid)
    db_op(sql4, db)

    # disconnect from server
    db.close()



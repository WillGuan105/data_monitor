#coding=utf-8
#!/usr/bin/python
from django.shortcuts import render
from django.http import HttpResponse
import os
import re
import logging
import sys
from difflib import *
import urllib
import json
import time
from django.db.models import Q
from .models import *
from django.core.exceptions import ObjectDoesNotExist

tuangou_url="http://www.meilishuo.com/tuan/?frm=daeh"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FILE="%s/webpagetest/defaulttwitterid.txt" % (BASE_DIR)
PC_FILE="%s/webpagetest/pctwitterid.txt" % (BASE_DIR)
MOB_FILE="%s/webpagetest/mobtwitterid.txt" % (BASE_DIR)
#pc凑单页（承接9.9疯抢）接口
pc_base_url='http://groupon.mlapi.meilishuo.com/miaosha/Miaosha_Pc_Activity_goods_list?event_id=2052'
#mob9.9疯抢接口
mob_base_url='http://groupon.mlapi.meilishuo.com/groupon/Groupon_poster_mob_for_event?event_id=2052'

def tuangou(request):
	cmd = 'curl ' + tuangou_url
	pagestr=os.popen(cmd).read()

	loadStr=""
	showStr=""
	loadCount=load_count(pagestr)
	if loadCount:
		loadStr="success"
	else:
		loadStr="fail"

	showCount=show_count(pagestr)

	if showCount:
		showStr="success"
	else:
		showStr="fail"

	restr="tuancount: " + loadStr + ", tuanpic: " + showStr
	return HttpResponse(restr)

def tuangou_gz(request):
	cmd = 'curl -H "host:www.meilishuo.com" 183.60.189.52/tuan'
	pagestr=os.popen(cmd).read()

	loadStr=""
	showStr=""
	loadCount=load_count(pagestr)
	if loadCount:
		loadStr="success"
	else:
		loadStr="fail"

	showCount=show_count(pagestr)

	if showCount:
		showStr="success"
	else:
		showStr="fail"

	restr="tuancount: " + loadStr + ", tuanpic: " + showStr
	return HttpResponse(restr)

def load_count(restr):
	
	goalstr='href="/share'
	count=restr.count(goalstr)
	if (count >= 12):
		return True
	else:
		return False

def show_count(restr):
	pattern = re.compile(r'.*共有.*p_total.*>\d{3}<.*件优质商品')
	match = pattern.match(restr)
	if match:
		return True
	else:
		return False

def groupon_poster_gz(request):
	cmd='curl -H "Host:groupon.mlapi.meilishuo.com" 10.0.0.55/groupon/groupon_poster'
	re=os.popen(cmd).read()
	reStatus="success"
	if re.find('"error_code":0') < 0:
		reStatus="fail"
	return HttpResponse(reStatus)

def getCurrenttime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

def newrunsame(request,cid,ptype):
    arObj=getObject(cid)#不存在处理
    url = arObj.c_baseurl+arObj.c_params

def newrunsame(request):
    #价格为tab，目前取值为1～4
    cid = request.GET.get('cid')
    rstr = ''

    arObj=getObject(cid)
    if not arObj:
        rstr = 'No cid = %s Check Item!'%cid
        return HttpResponse(rstr)
    if arObj.c_type =='pc':
        FILE=PC_FILE
    elif arObj.c_type =='mob':
        FILE=MOB_FILE
    else:
        FILE=DEFAULT_FILE

    url=arObj.c_baseurl+'?'+arObj.c_params
    #otherparams=["frame_num","total"]
    otherparams=eval(arObj.c_otherparams)
    path=eval(arObj.c_path)
    (plist,erromes,isuse)=getTwitterIdList(url,arObj.c_type,otherparams,path)
    #erromes = 'abc'
    rstr = rstr+findSameGoods(plist)

    if rstr and isuse :
        rstr = "%s There are same goods!<br> %s url is %s<br><br> isuse is %s<br>error message is %s"%(getCurrenttime(),arObj.c_type,url,isuse,erromes)+rstr
        f = open(FILE,'a')
        print >> f,'%s %s url is %s \n rstr is %s \n errormess is %s \n list is %s'%(getCurrenttime(),arObj.c_type,url,rstr,erromes,plist)
        f.close()
    else:
        rstr = "%s There are not same goods!<br> %s url is %s<br> <br>isuse is %s<br> error message is %s"%(getCurrenttime(),arObj.c_type,url,isuse,erromes)
    return HttpResponse(rstr)

def getObject(cid):
		try:
			ar = checkDiffItems.objects.get(c_ID=cid)
			return ar
		except ObjectDoesNotExist:
			return None

def getTwitterIdList(url,ptype,otherparams,path):
    isuse=True
    erromes='null'
    alist=[]
    data=getPageJson(url)
    start=0

    '''
    if ptype =='pc':
        start = 1
    else:
        start =0
    '''


    if data.has_key('error_code') and data['error_code'] !=0:
        erromes= 'error_code is not zero'
        #return erromes

    if 'frame_size' in otherparams:
        frame_num = getTotalframe(data)
        print "frame_num=%s%%%%%%%%%%%%%%%%%%%%%%"%frame_num
        if frame_num == -1:
            erromes='data is empty!'
            return alist,erromes
        if frame_num == -2:
            erromes= 'frame_size is null or 0!'
            return alist,erromes
        if frame_num == -3:
            erromes= 'total_num is null!'
            return alist,erromes
        if frame_num == 0:
            erromes= 'There is no goods!'
            return alist,erromes
    else:
        frame_num = 1

    (realpath,listdict,count,isempty)=getRealPath(path,url)
    rplist=realpath.split("#")
    plist=path["path"].split("#")
    if rplist[-1]!= plist[-1]:
        erromes = 'Pointed path is %s!Real path is %s !The Interface is empty!'%(path["path"],realpath)
    print '+++++++++++++++++++++++'
    print listdict

    firstsrc = 'cache'
    cursrc = 'cache'
    for num in range(start,frame_num):
        now_url = url + '&frame=%s'%num
        print 'now_url=%s&&&&&&&&&&&&'%(now_url)
        pdata=getPageJson(now_url)
        #print "rplist is %s &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"%rplist
        valStr='pdata'
        nowpathdict={}

        if pdata.has_key('data') and isinstance(pdata['data'],dict) and pdata['data'].has_key('source'):
            if num == start:
                firstsrc = pdata['data']['source']
            else:
                cursrc = pdata['data']['source']

        if num != start:
            if 'cache' in firstsrc and 'db' in cursrc:
                isuse=False
            if 'cache' in firstsrc and 'cache' in cursrc and cursrc != firstsrc:
                firstt=int(firstsrc.split(":")[2])+float(firstsrc.split(":")[3])/60.0
                curt=int(cursrc.split(":")[2])+float(cursrc.split(":")[3])/60.0
                if curt-firstt >= 2.0:
                    isuse=False
            if 'db' in firstsrc and 'db' in cursrc and cursrc != firstsrc:
                firstt=int(firstsrc.split(":")[2])+float(firstsrc.split(":")[3])/60
                curt=int(cursrc.split(":")[2])+float(cursrc.split(":")[3])/60.0
                if curt-firstt >= 2.0:
                    isuse=False

        if not isuse:
            return alist,erromes,isuse


        listdict=getRealPath(path,now_url)[1]
        print "listdict is ",listdict
        print '##############################'
        isempty=getRealPath(path,now_url)[3]
        #if len(listdict) <=1:
        if isempty:
            continue

        print count
        for i in range(0,count):
            a='num'+str(i)
            nowpathdict[a]=[]
        print nowpathdict

        k=0
        for p in rplist:
            a='num'+str(k)
            b='num'+str((k+1))
            if p == 'pdata':
                nowpathdict[a]=["pdata"]
                continue
            if not listdict.has_key(p):
                valStr+="['%s']" % p
                #nowpathdict[a].append(valStr)
                #nowpathdict[a]=[valStr]
                for i in range(len(nowpathdict[a])):
                    nowpathdict[a][i]+="['%s']" % p
            elif p == b:
                #print "enter p=b,p is%s,b is %s"%(p,b)
                for j in range(listdict[a]):
                    for i in range(listdict[b]):
                        #print  "range(listdict[b]) is %s@@@@@@@@@@@@@@@@@@"%range(listdict[b])
                        np=nowpathdict[a][j]+"[%s]" % str(i)
                        nowpathdict[b].append(np)
                    print nowpathdict[b]
                k+=1

        endpath= 'num'+str(len(listdict)-1)


        for i in range(len(nowpathdict[endpath])):
            p=nowpathdict[endpath][i]
            print "p is %s #################################"%p
            val=eval(p)
            print val
            alist.append(val)
    print alist
    print "len(alist)is%s@@@@@@@@@@@@@@@@@@"%len(alist)
    return alist,erromes,isuse

def getRealPath(path,now_url):
    pdata=getPageJson(now_url)
    pathlist=path['path'].split("#")
    realpath='pdata'
    listdict={}
    listdict['num0']=1
    valStr='pdata'
    count=1
    isempty = False
    for p in pathlist:
        valStr+="['%s']" % p
        realpath = realpath+'#'+p
        print "valStr is %s ***************"%valStr
        rpath=eval(valStr)
        if not rpath:
            isempty = True
            return (realpath,listdict,count,isempty)
        if isinstance(rpath,list):
            if len(rpath) == 0:
                isempty = True
                print '%s list is empty'%(valStr)
                return (realpath,listdict,count,isempty)

            k='num'+str(count)
            realpath=realpath+'#'+k
            valStr+="[0]"
            listdict[k]=len(rpath)
            count+=1
    print 'listdict is %s &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'%listdict
    return (realpath,listdict,count,isempty)



def findSameGoods(plist):
    print "enter finds**********************"
    rstr=''
    if not plist:
        return rstr
        #exit('list is empty')
    print "len(plist)is %s!!!!!!!!!!!!!!!!!!!!!!!"%len(plist)
    for i in range(len(plist)):
        if plist.count(plist[i]) > 1:
            print '%s has same goods,total_number is %s'%(plist[i],plist.count(plist[i]))
            rstr= rstr+'<br>%s has same goods,total_number is %s!<br>'%(plist[i],plist.count(plist[i]))
        else:
            print '%s number is one'%(plist[i])
    return rstr

def diffPCMob(pcurl,moburl):
    if not pcurl:
        exit('pcurl is empty')
    if not moburl:
        exit('moburl is empty')
    rstr=''
    pclist=getTwitterIdList(pcurl,'pc')
    f = open(PC_FILE,'a')
    print >> f,'%s pcurl is %s \n pclist is %s'%(getCurrenttime(),pcurl,pclist)
    f.close()
    moblist=getTwitterIdList(moburl,'mob')
    f = open(MOB_FILE,'a')
    print >> f,'%s moburl is %s \n moblist is %s'%(getCurrenttime(),moburl,moblist)
    f.close()
    if not cmp(pclist,moblist):
        print 'PC same as MOB!'
        rstr = "<br>PC same as MOB!<br>"
    else:
        rstr = "<br>PC different from  MOB!!<br>"
        if len(pclist) > len(moblist):
            #print 'PC has more goods than MOB'
            rstr = rstr+"<br>PC has more goods than MOB<br>"+findDiffgoods(pclist,moblist,len(moblist))
        elif len(pclist) < len(moblist):
            #print 'mob has more goods than pc'
            rstr = rstr+"<br>PC has more goods than MOB<br>"+findDiffgoods(pclist,moblist,len(pclist))
        else:
            #print 'goods number is same'
            rstr = rstr+"<br>goods number is same in PC and MOB!<br>"+findDiffgoods(pclist,moblist,len(pclist))
    return rstr

#比较pc凑单页和mob端9.9疯抢是否商品一致
def rundiff(request):
    #价格为tab，目前取值为1～4
    rstr=''
    for i in range(1,5):
        pc_baseurl = pc_base_url +'&tab=%s'%(i)
        mob_baseurl = mob_base_url +'&tab=%s'%(i)
        for j in range(0,5):
            if j ==2:
                continue
            elif j==4:
                for t in range(2):
                    pcurl = pc_baseurl +'&sbase=%s&sort=%s'%(j,t)
                    moburl = mob_baseurl +'&sbase=%s&sort=%s'%(j,t)
                    rstr='<br>%s pcurl is %s<br><br>moburl is %s<br>'%(getCurrenttime(),pcurl,moburl)+diffPCMob(pcurl,moburl)+rstr
            else:
                pcurl = pc_baseurl +'&sbase=%s&sort=0'%(j)
                moburl = mob_baseurl +'&sbase=%s&sort=0'%(j)
                print 'pcurl=%s'%(pcurl)
                print 'moburl=%s'%(moburl)
                rstr='<br>%s pcurl is %s<br><br>moburl is %s<br>'%(getCurrenttime(),pcurl,moburl)+diffPCMob(pcurl,moburl)+rstr
    #print 'done'
    return HttpResponse(rstr)

#比较pc凑单页是否有重复商品

def runsame(request,ptype):
    #价格为tab，目前取值为1～4
    rstr = ''
    samegoodsurl=''
    base_url=''
    FILE=''
    if ptype =='pc':
        base_url = pc_base_url
        FILE=PC_FILE
    elif ptype =='mob':
        base_url = mob_base_url
        FILE=MOB_FILE
    for i in range(1,5):
        baseurl = base_url +'&tab=%s'%(i)
        #pc_baseurl = pc_base_url +'&tab=%s'%(i)
        #mob_baseurl = mob_base_url +'&tab=%s'%(i)
        for j in range(0,5):
            if j ==2:
                continue
            elif j==4:
                for t in range(2):
                    url=baseurl +'&sbase=%s&sort=%s'%(j,t)
                    #pcurl = pc_baseurl +'&sbase=%s&sort=%s'%(j,t)
                    #moburl = mob_baseurl +'&sbase=%s&sort=%s'%(j,t)
                    #diffPCMob(pcurl,pcurl)
                    print 'j=4,url=%s'%(url)
                    plist=oldgetTwitterIdList(url,ptype)
                    rstr = rstr+findSameGoods(plist)
                    newrstr= findSameGoods(plist)
                    if newrstr:
                        samegoodsurl+= url
                        f = open(FILE,'a')
                        print >> f,'%s %s url is %s \n list is %s'%(getCurrenttime(),ptype,url,plist)
                        f.close()

            else:
                url = baseurl +'&sbase=%s&sort=0'%(j)
                #moburl = mob_baseurl +'&sbase=%s&sort=0'%(j)
                print 'url=%s'%(url)
                #print 'moburl=%s'%(moburl)
                #diffPCMob(pcurl,pcurl)
                plist=oldgetTwitterIdList(url,ptype)
                rstr = rstr+findSameGoods(plist)
                newrstr = findSameGoods(plist)
                if newrstr:
                    samegoodsurl+=url
                    f = open(FILE,'a')
                    print >> f,'%s %surl is %s \n list is %s'%(getCurrenttime(),ptype,url,plist)
                    f.close()

    if not rstr:
        rstr = "%s There are not same goods!<br> %s base_url is %s<br>"%(getCurrenttime(),ptype,base_url)
    else:
        rstr = "%s There are same goods!<br> %s base_url is %s<br><br> The url is %s<br>"%(getCurrenttime(),ptype,base_url,samegoodsurl)+rstr
    return HttpResponse(rstr)

def oldgetTwitterIdList(url,ptype):
	data=getPageJson(url)

	if ptype =='pc':
		start = 1
	elif ptype =='mob':
		start =0

	if data['error_code'] !=0:
		exit('error_code is not zero')
	else:
		frame_num = getTotalframe(data)+1
        #print 'frame_num=%s!!!!!!!!!!!!!!!!!!!!!!'%frame_num
        alist=[]
        if frame_num > 1:
            for num in range(start,frame_num):
                now_url = url + '&frame=%s'%num
                #print 'now_url=%s&&&&&&&&&&&&'%(now_url)
                pdata=getPageJson(now_url)
                goods_num=len(pdata['data']['tInfo'])
                print 'goods_num=%s-------------------'%(goods_num)
                for i in range(goods_num):
                    alist.append(pdata['data']['tInfo'][i]['twitter_id'])
        return alist

def findDiffgoods(pclist,moblist,len):
    rstr=''
    for i in range(len):
        if pclist[i] != moblist[i]:
            #print '%sth goods is different!PC is %s,Mob is %s'%(i+1,pclist[i],moblist[i])
            rstr=rstr+'<br>%sth goods is different!PC is %s,Mob is %s<br>'%(i+1,pclist[i],moblist[i])
    return rstr

def getPageJson(url):
    print "url is %s++++++++++++"%url
    if not url:
        Ddata = 'null'

    page=urllib.urlopen(url)
    data=page.read()
    Ddata=json.loads(data)
    return Ddata

def getTotalframe(data):
    if not data:
        frame_num = -1

    totalNum = data['data']['totalNum']
    print 'totalNum=%s************'%totalNum
    frame_size = data['data']['frame_size']
    print 'frame_size=%s************'%frame_size

    if not frame_size:
        frame_num = -3

    if not frame_size or frame_size == 0:
        frame_num = -2

    if frame_size !=0 and totalNum %frame_size !=0:
        frame_num = (totalNum /frame_size) +1
    if frame_size !=0 and totalNum %frame_size ==0:
        frame_num = totalNum /frame_size
    return frame_num

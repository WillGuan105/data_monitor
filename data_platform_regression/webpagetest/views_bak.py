#coding=utf-8
#!/usr/bin/python
from django.shortcuts import render
from django.http import HttpResponse
import os
import re

tuangou_url="http://www.meilishuo.com/tuan/?frm=daeh"

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




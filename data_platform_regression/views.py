#coding=utf-8
#!/usr/bin/python

from django.http import HttpResponse
import os
import re

tuangou_url="http://www.meilishuo.com/tuan/?frm=daeh"

def tuangou(request):
	loadStr=""
	showStr=""
	loadCount=load_count()
	if loadCount:
		loadStr="success"
	else:
		loadStr="fail"

	showCount=show_count()

	if showCount:
		showStr="success"
	else:
		showStr="fail"

	restr="tuancount: " + loadCount + ", tuanpic: " + showCount
	return HttpResponse(restr)

def load_count():
	cmd = 'curl ' + tuangou_url
	restr=os.popen(cmd).read()
	goalstr='href="/share'
	count=restr.count(goalstr)
	if (count > 20):
		return True
	else:
		return False

def show_count():
	pattern = re.compile(r'.*共有.*p_total.*>\d{3}<.*件优质商品')
	match = pattern.match(restr)
	if match:
		return True
	else:
		return False



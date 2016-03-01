#coding=utf-8
import urllib2
import os
import json
import pycurl
import StringIO
from hashlib import md5
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os,time
import sys
import shutil

def md5_file(name):
	m = md5()
	a_file = open(name, 'rb')    
	m.update(a_file.read())
	a_file.close()
	return m.hexdigest()
if __name__ == '__main__':
	if len(sys.argv) <> 4:
		print 'param count error'
		exit(1)
	if sys.argv[1] == '' or sys.argv[2] == '' or sys.argv[3] == '':
		print 'param error'
		exit(1)
	else:
		reportId = sys.argv[1]
		start_date = sys.argv[2]
		end_date = sys.argv[3]
	options = webdriver.ChromeOptions()
	options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
	driver = webdriver.Chrome('/home/data/xiaoyao/downPNG/chromedriver',chrome_options=options)
	driver.get('http://data.meiliworks.com:9527/report/showreport/'+reportId+'?toDownPng=1');
	driver.add_cookie({'name':'down_png_request', 'value':md5_file('../data/md5.key')})
	driver.get("http://data.meiliworks.com:9527/report/showreport/"+reportId+"?toDownPng=3&start_date="+start_date+'&end_date='+end_date);
	time.sleep(12)
	driver.find_element_by_id("downData").click()
	driver.find_element_by_id("png").click()
	driver.find_element_by_id("download").click()
	time.sleep(10)
	shutil.copy('/home/data/Downloads/test_'+reportId+'_'+start_date+'_'+end_date+'.png','/home/data/xiaoyao/testPNG/test/savePNG')
	driver.quit()

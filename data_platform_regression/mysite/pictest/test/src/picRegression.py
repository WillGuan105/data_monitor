#ecoding=utf-8
import os
from picComDiff import *

save_path='/home/data/xiaoyao/testPNG/test/savePNG/'
diff_path='/home/data/xiaoyao/testPNG/test/diffPNG/'
stand_path='/home/data/xiaoyao/testPNG/test/standPNG/'

def removeOldPng():
	if len(os.listdir(save_path)) != 0:
		os.system('rm ' + save_path + '*')
	if len(os.listdir(diff_path)) != 0:	
		os.system('rm ' + diff_path + '*')

def getDownList():
	cur_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	cur_sep=os.sep
	down_list=cur_path+cur_sep+"data"+cur_sep+"down_list.txt"
	down_file=open(down_list)
	line=down_file.readline()
	run_list=[]
	while line.strip():
		run_list.append(line.strip())
		down_cmd="DISPLAY=:0 /usr/bin/python downTestPng.py %s" % (line)
		os.system(down_cmd)
		line=down_file.readline()
	return run_list

def comAllPics():
	result_dict={}
	cmp_list=getDownList()
#	cmp_list=['761 2015-07-20 2015-07-20', '499 2015-07-20 2015-07-20']
	for cur_report in cmp_list:
		cur_report = "test " + cur_report
		tmp=cur_report.split(" ")
		reportId=tmp[1]
		cur_report = '_'.join(tmp)
		cur_report = cur_report + ".png"
		result_pic=save_path + cur_report
		stand_pic=stand_path + cur_report
		diff_pic=diff_path + reportId + ".png"
		ret=comPic(result_pic,stand_pic,diff_pic)
		result_dict[reportId]=ret
        print result_dict
		
	
	
removeOldPng()
#getDownList()
comAllPics()

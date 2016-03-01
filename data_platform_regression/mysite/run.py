#!coding:utf-8
import os
from difflib import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(result_id,g_id,url):
    re_file="%s/mysite/result/%s.txt" % (BASE_DIR,g_id)
    stand_file="%s/mysite/stand/%s.txt" % (BASE_DIR,g_id)
    httpUrl=url.split("?")[0]
    params=url.split("?")[1]
    cmd="curl \"%s\" -d \"%s\" > %s" % (httpUrl,params,re_file)
    print cmd
    os.system(cmd)

    dif_ret=compFile(stand_file,re_file)
    if (dif_ret!=0):
        diff_file="%s/static/datadiff/%s_%s.html" % (BASE_DIR,result_id,g_id)
        cmd = 'touch %s' % (diff_file)
        os.system(cmd)
        if os.path.exists(diff_file):
            fp=open(diff_file,'w+')
        fromfile=open(stand_file,'r').readlines()
        tofile=open(re_file,'r').readlines()
        diffhtml=HtmlDiff.make_file(HtmlDiff(),fromfile,tofile)
        diffhtml=('''%s''') % (diffhtml)
        diffhtml=diffhtml.replace('<head>','<head><meta charset="UTF-8">',1)
        diffhtml=diffhtml.replace('<td class="diff_next">','</tr><tr><td class="diff_next">',1)
        diffhtml=diffhtml.replace('nowrap="nowrap"','')
        diffhtml=diffhtml.replace('cellspacing="0" cellpadding="0" rules="groups"','border="1"')
        diffhtml=diffhtml.replace('1</td>','预期结果',1)
        diffhtml=diffhtml.replace('1</td>','实际结果',1)
        fp.write(diffhtml)
        fp.close()
        # cmd="diff %s %s > %s" % (stand_file,re_file,diff_file)
        # os.system(cmd)

    return dif_ret


def compFile(stand,result):
    cmd="diff %s %s" % (stand,result)
    ret=os.system(cmd)
    return ret

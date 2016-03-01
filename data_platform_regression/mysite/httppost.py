#!/usr/bin/env python
#coding=utf8
 
import httplib, urllib
 
httpClient = None
try:
    params = urllib.urlencode({'shop_id': '100014'})
    headers = {"Meilishuo": "uid:1178834;ip:123"}
 
    httpClient = httplib.HTTPConnection("viruslab.meilishuo.com/focus/Read_shop_type", 80, timeout=30)
    httpClient.request("POST", "/test.php", params, headers)
 
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
    print response.getheaders() #获取头信息
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()
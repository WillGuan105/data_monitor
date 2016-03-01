#coding:utf-8

import urllib
import urllib2
import httplib
import json

WEB_URL = url="http://alarm.meiliworks.com/api/push"

class Monitor:
    _arr = {};

    '''
    构造函数
    token：由monitor平台获取的监控组token值，所有监控项信息推送到该监控组
    '''
    def __init__(self, token):
        self._arr = {
            "token": token,
            "type": 1,
            "items": [],
        }

    '''
    添加pass的监控项信息
    name: 必填，监控项名，监控组里的唯一值，用简短有意义的短语
    custom：可填，自定义告警信息
    '''
    def add_pass(self, name, custom=""):
        self._add_item(name, 1, custom)

    '''
    添加fail的监控项信息
    name: 必填，监控项名，监控组里的唯一值，用简短有意义的短语
    custom：可填，自定义告警信息
    '''
    def add_fail(self, name, custom=""):
        self._add_item(name, 0, custom)

    #上报告警信息，返回码code=0时为推送失败，1为推送成功
    def report(self):
        return self._post_data(WEB_URL, self._arr)

    #内部方法
    def _add_item(self, name, status, custom=""):
        self._arr["items"].append({
            "name":name,
            "status":status,
            "custom":custom,
        })

    #内部方法
    def _post_data(self, url, data):
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        return json.loads(response.read())

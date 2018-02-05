#!/usr/bin/python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: common.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-06-27 14:59:10
############################

import json
import os
import configparser
import sys
import re

#解析配置文件
cwd = os.path.split(os.path.realpath(__file__))[0]
cfg = cwd + "/../conf.ini"
config = configparser.ConfigParser()
config.read(cfg)   # 注意这里必须是绝对路径

cmdb_url=config.get("cmdb", "url")

sys.path.append('../')
from libs.functions import *

def parseUrl(url):
	o = url.split('/')
	location = '/'.join(o[3:])
	domain = o[2]
	return [domain,location]

def typeUrl(msg):
	app = msg['app']
	org_id, check = checkThreshold("url", "app", app, msg['value'])

	newmsg = {}
	newmsg['类型'] = "url"
	newmsg['名称'] = msg['url']

	newmsg['主题'] = "URL监控-" + app + "接口访问异常"
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['严重性'] = msg['severity']
	newmsg['监控点'] = msg['monitor_node']
	newmsg['APP'] = app
	newmsg['数据'] = []
	url_cmdb = "CMDB配置: &nbsp;<a href=\"" + cmdb_url + "/pages/UI.php?operation=details&class=Url&id=" + \
			msg['cmdbid'] + "\">" + msg['cmdbid'] + "</a><br>" + "Location:&nbsp;" + parseUrl(msg['url'])[1]

	data = {"URL":url_cmdb, "Value(配置/实际)":msg['value'], 
			"故障时间":msg['downtime'], "当前时间":msg['datetime'],
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = str(org_id) + "_" + msg['severity'] + "." + msg['status'] + "." + msg['monitor_node'] + "." + app + ".json"
	file_db = file_db.replace(" ","-").replace("/","_").replace(":","_")
	
	ret = {}
	ret['file_db'] = file_db
	ret['data'] = newmsg
	return(ret)

if __name__ == '__main__':
	msg = sys.argv[1]
	print(json.dumps(typeUrl(initMsg(msg))))

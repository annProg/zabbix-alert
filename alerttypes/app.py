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
import sys
import re

sys.path.append('../')
from libs.functions import *

def typeApp(msg):
	app = msg['itemkey'].split('[')[1].split(']')[0]

	# 匹配带了端口的upstream名称
	m = re.match(r'\w+([-_]\w+\d*)*\.\d+$', app)
	if m:
		app = app.split('.')
		app = app[0:-1]
		app = ".".join(app)

	itemtype = msg['itemkey'].split('[')[0]

	if msg['itemkey2'].split('[')[0] == "http_499":
		itemvalue = msg['itemvalue2'] + "/" + msg['itemvalue']
		itemkey = msg['itemkey2'] + "/" +msg['itemkey']
		itemtype = msg['itemkey2'].split('[')[0]
	else:
		itemvalue = msg['itemvalue']
		itemkey = msg['itemkey']

	if msg['status'] == "PROBLEM":
		downtime = msg['downdate'] + " " + msg['downtime']
	else:
		if msg['downdate'] == msg['update']:
			downtime = msg['downdate'] + " " + msg['downtime']  + "--" + msg['uptime']
		else:
			downtime = msg['downdate'] + " " + msg['downtime'] + " - " + msg['update'] + " " + msg['uptime']

	newmsg = {}
	org_id, check = checkThreshold(itemkey, "app", app, itemvalue)
	# 未达到阈值直接退出
	if not check:
		filterlog("threshold filtered", "", msg['name'])
		ack(msg['eventid'])
		return False

	newmsg['eventid'] = msg['eventid']
	newmsg['类型'] = "app"
	newmsg['名称'] = app
	newmsg['主题'] = msg['name']
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['严重性'] = msg['severity']
	newmsg['监控项'] = itemkey
	newmsg['数据'] = []
	data = {"主机":msg['hostname'], "Value":itemvalue, "严重性":msg['severity'], 
			"故障时间":downtime, "当前时间":msg['date'] + " " + msg['time'], 
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = str(org_id) + "_" + msg['severity'] + "." + msg['status'] + "." + msg['name'] + ".json"
	file_db = file_db.replace(" ","-").replace("/","_")
	
	ret = {}
	ret['file_db'] = file_db
	ret['data'] = newmsg
	return(ret)

if __name__ == '__main__':
	msg = sys.argv[1]
	print(json.dumps(typeApp(initMsg(msg))))

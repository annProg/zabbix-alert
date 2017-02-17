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

def typeUpstream(msg):
	# cmdbApi中type用app，从upstream名称中截取出app名称
	# newmsg['类型'] 需要设置为 app，以便调用cmdbApi获取联系人
	app = msg['itemname']
	# 匹配upstream名称
	m = re.match(r'.*?:\s(.*\/)?(.*?)\.conf\-\-.*', app)
	if m:
		app = m.group(2)

	# 去掉upstream端口
	app = app.replace("upstream-","")
	m = re.match(r'\w+([-_]\w+\d*)*\-\d+$', app)
	if m:
		app = app.split('-')
		app = app[0:-1]
		app = "-".join(app)


	if msg['status'] == "PROBLEM":
		downtime = msg['downdate'] + " " + msg['downtime']
	else:
		if msg['downdate'] == msg['update']:
			downtime = msg['downdate'] + " " + msg['downtime']  + "--" + msg['uptime']
		else:
			downtime = msg['downdate'] + " " + msg['downtime'] + " - " + msg['update'] + " " + msg['uptime']

	trigger = msg['name'].split(":")
	triggername = trigger[0] + "-" + trigger[1]
	triggername = triggername.replace(" ", "-").replace("，", "-")

	item = msg['itemkey'].split(",")
	itemkey = item[1] + ":" + item[2]
	itemkey = itemkey.replace("]", "")

	if msg['itemvalue'] == "0":
		itemvalue = "Down"
	else:
		itemvalue = "Up"

	newmsg = {}
	newmsg['eventid'] = msg['eventid']
	newmsg['类型'] = "app"
	newmsg['名称'] = app
	newmsg['主题'] = triggername
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['严重性'] = msg['severity']
	newmsg['数据'] = []
	data = {"主机":msg['hostname'] + "<br>" + msg['ip'], "Docker":itemkey, "Value":itemvalue, 
			"严重性":msg['severity'], 
			"故障时间":downtime, "当前时间":msg['date'] + " " + msg['time'], 
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = newmsg['严重性'] + "." + msg['status'] + ".upstream异常." + newmsg['类型'] + "." + app + ".json"
	file_db = file_db.replace(" ","-").replace("/","_")
	
	ret = {}
	ret['file_db'] = file_db
	ret['data'] = newmsg
	return(ret)

def initMsg(msg):
	msg = msg.replace("'", '"')
	msg = json.loads(msg)
	return msg

if __name__ == '__main__':
	msg = sys.argv[1]
	print(json.dumps(typeUpstream(initMsg(msg))))

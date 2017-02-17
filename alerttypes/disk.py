#!/usr/bin/python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: common.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-06-27 14:59:10
############################

'''
copy from default.py
仅强制修改db文件名中的severity为Information，用于磁盘报警延迟发送.
reduce.py中匹配磁盘告警触发器名称
'''

import json
import os
import sys
import re

def typeDisk(msg):
	grp = msg['hostgroup']
	name = msg['hostname']

	if msg['status'] == "PROBLEM":
		downtime = msg['downdate'] + " " + msg['downtime']
	else:
		if msg['downdate'] == msg['update']:
			downtime = msg['downdate'] + " " + msg['downtime']  + "--" + msg['uptime']
		else:
			downtime = msg['downdate'] + " " + msg['downtime'] + " - " + msg['update'] + " " + msg['uptime']

	trigger = " ".join(msg['name'].split(" ")[0:2]).split("，")[0]

	newmsg = {}
	newmsg['eventid'] = msg['eventid']
	newmsg['类型'] = "disk"
	newmsg['名称'] = name
	newmsg['IP'] = msg['ip']
	newmsg['严重性'] = msg['severity']
	newmsg['主题'] = trigger
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['数据'] = []
	data = {"IP":msg['ip'],  "监控项":msg['itemkey'], "Value":msg['itemvalue'], 
			"严重性":msg['severity'], "故障时间":downtime, 
			"当前时间":msg['date'] + " " + msg['time'], 
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = "Information." + msg['status'] + "."  + newmsg['类型'] + "." + trigger + ".json"
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
	print(json.dumps(typeDisk(initMsg(msg))))

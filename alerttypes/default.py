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

def typeDefault(msg):
	grp = msg['hostgroup']
	name = msg['hostname']

	downtime = getDownTime(msg)

	trigger = " ".join(msg['name'].split(" ")[0:2]).split("，")[0]

	newmsg = {}
	org_id, check = checkThreshold(msg['itemkey'], "ip", msg['ip'], msg['itemvalue'])
	# 未达到阈值直接退出
	if not check:
		filterlog("threshold filtered", "", msg['name'])
		ack(msg['eventid'])
		return False

	newmsg['eventid'] = msg['eventid']
	newmsg['类型'] = "default"
	newmsg['名称'] = name
	newmsg['IP'] = msg['ip']
	newmsg['严重性'] = msg['severity']
	newmsg['主题'] = trigger
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['数据'] = []
	data = {"IP":msg['ip'],  "监控项":msg['itemname'], "Value":msg['itemvalue'], 
			"严重性":msg['severity'], "故障时间":downtime, 
			"当前时间":getDateTime(msg), 
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = str(org_id) + "_" + msg['severity'] + "." + msg['status'] + "."  + newmsg['类型'] + "." + trigger + ".json"
	file_db = file_db.replace(" ","-").replace("/","_")
	
	ret = {}
	ret['file_db'] = file_db
	ret['data'] = newmsg
	return(ret)

if __name__ == '__main__':
	msg = sys.argv[1]
	print(json.dumps(typeDefault(initMsg(msg))))

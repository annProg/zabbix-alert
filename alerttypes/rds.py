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

def typeRds(msg):
	grp = msg['hostgroup']
	name = msg['hostname']

	downtime = getDownTime(msg)

	trigger = " ".join(msg['name'].split(" ")[0:2]).split("，")[0]

	newmsg = {}
	newmsg['eventid'] = msg['eventid']
	newmsg['类型'] = "rds"
	newmsg['名称'] = name
	newmsg['严重性'] = msg['severity']
	newmsg['主题'] = trigger
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['数据'] = []
	data = {"Value":msg['itemvalue'], 
			"故障时间":downtime, 
			"当前时间":getDateTime(msg), 
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = msg['severity'] + "." + msg['status'] + "."  + newmsg['类型'] + "." + trigger + ".json"
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
	print(json.dumps(typeRds(initMsg(msg))))

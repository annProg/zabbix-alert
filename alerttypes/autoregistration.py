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


'''
zabbix配置默认信息
{'date':'{DATE}', 'time':'{TIME}', 'ip':'{HOST.IP}','hostname':'{HOST.HOST}', 'port':'{HOST.PORT}','hostgroup':'AutoRegistration','name':'{ACTION.NAME}'}
'''

def typeAutoRegistration(msg):
	grp = msg['hostgroup']
	name = msg['hostname']
	ip = msg['ip']
	port = msg['port']
	actionname = msg['name']

	newmsg = {}
	newmsg['类型'] = "zabbix自动注册"
	newmsg['名称'] = name
	newmsg['IP'] = msg['ip']
	newmsg['严重性'] = "Notice"
	newmsg['主题'] = "zabbix监控自动注册:" + actionname
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">OK</span>"
	newmsg['数据'] = []
	data = {"IP":msg['ip'],"严重性":"Notice",
			"当前时间":msg['date'] + " " + msg['time']}
	newmsg['数据'].append(data)

	file_db = newmsg['类型'] + "-" + actionname + ".json"
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
	print(json.dumps(typeAutoRegistration(initMsg(msg))))

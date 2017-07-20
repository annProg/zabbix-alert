#!/usr/bin/python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: extends.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-06-27 14:59:10
############################

'''
{
'type':'',   // 类型 可选 app, ip
'name':'',   //app名称,或者ip地址,必须在cmdb存在
'status':'', //报警状态, PROBLEM,OK
'severity':'', //严重程度 Information,Warning,Average,High,Disaster  其中High,Disaster发短信
'start': '',   //故障开始时间
'now': '',     //当前时间
'age': '',     //故障时长
'id': '',      //报警ID
'itemkey': '',   //监控项
'itemvalue': '', //监控项值
'title': '',     //标题
'description': '', //描述
}
'''

import json
import os
import sys
import re

def typeExtends(msg):
	newmsg = {}
	newmsg['ID'] = msg['id']
	newmsg['类型'] = msg['type']
	newmsg['名称'] = msg['name']
	newmsg['严重性'] = msg['severity']
	newmsg['主题'] = msg['name'] + " - " + msg['title']
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['数据'] = []
	data = {"name":msg['name'],  "监控项":msg['itemkey'], "Value":msg['itemvalue'], 
			"严重性":msg['severity'], "故障时间":msg['start'], 
			"当前时间":msg['now'],
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"
			}
	newmsg['数据'].append(data)

	file_db = msg['severity'] + "." + msg['title'] + "." + msg['status'] + "."  + msg['type'] + "." + msg['name'] + ".json"
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
	print(json.dumps(typeExtends(initMsg(msg))))

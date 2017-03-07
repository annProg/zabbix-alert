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

def typeUrl(msg):
	app = msg['app']

	newmsg = {}
	newmsg['类型'] = "url"
	newmsg['名称'] = msg['url']

	newmsg['主题'] = "URL监控-" + app + "接口访问异常"
	newmsg['状态'] = "<span style=\"color:red; font-weight:bold;\">" + msg['status'] + "</span>"
	newmsg['严重性'] = msg['severity']
	newmsg['监控点'] = msg['monitor_node']
	newmsg['APP'] = app
	newmsg['数据'] = []
	url_cmdb = "<a href=\"" + cmdb_url + "/pages/UI.php?operation=details&class=Url&id=" + \
		msg['cmdbid'] + "\">" + "(" + msg['cmdbid'] + ")&nbsp;&nbsp;" + msg['url'] + "</a>"

	data = {"URL":url_cmdb, "Value":msg['value'], 
			"故障时间":msg['downtime'], "当前时间":msg['datetime'],
			"故障时长":"<span style=\"color:red; font-weight:bold;\">" + msg['age'] + "</span>"}
	newmsg['数据'].append(data)

	file_db = msg['severity'] + "." + msg['status'] + "." + msg['monitor_node'] + "." + app + ".json"
	file_db = file_db.replace(" ","-").replace("/","_").replace(":","_")
	
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
	print(json.dumps(typeUrl(initMsg(msg))))

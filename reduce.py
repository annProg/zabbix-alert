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
from libs.db import updateDB
from alerttypes.app import typeApp
from alerttypes.default import typeDefault
from alerttypes.upstream import typeUpstream
from alerttypes.disk import typeDisk
from alerttypes.load import typeLoad
from alerttypes.url import typeUrl
from alerttypes.rds import typeRds
from alerttypes.autoregistration import typeAutoRegistration
import logging
import re

filepath = os.path.realpath(__file__)
fold = "%s/" % (os.path.dirname(filepath))

errlog = fold + "logs/reduce.log"
fold_new = fold + "new/"

#print(fold_new)

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=errlog)

def initMsg(msg):
	msg = msg.replace("'", '"')
	msg = json.loads(msg)
	return msg

def run(msg):
	hostgroup_app = "应用状态监控"
	hostgroup_rds = "RDS监控"
	upstream_app = re.match(r'^NGinx-Upstream:\s.*',msg['name'])  # Upstream检查
	is_disk = re.match(r'^文件系统:.*', msg['name']) # 磁盘空间告警
	is_load = re.match(r'^CPU: 负载过高.*', msg['name']) # 负载高告警

	if hostgroup_app in msg['hostgroup']:
		newmsg = typeApp(msg)
	elif hostgroup_rds in msg['hostgroup']:
		newmsg = typeRds(msg)
	elif upstream_app:
		newmsg = typeUpstream(msg)
	elif is_disk:
		newmsg = typeDisk(msg)
	elif is_load:
		newmsg = typeLoad(msg)
	elif msg['hostgroup'] == "url_monitor":
		newmsg = typeUrl(msg)
	elif msg['hostgroup'] == "AutoRegistration":
		newmsg = typeAutoRegistration(msg)
	else:
		newmsg = typeDefault(msg)

	path = fold_new + newmsg['file_db']
	updateDB(path, newmsg['data'])

if __name__ == '__main__':
	try:
		msg = initMsg(sys.argv[3])
		run(msg)
	except:
		logging.exception("Exception Logged")

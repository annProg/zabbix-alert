#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: alertrule.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2017-11-08 17:30:52
############################

import configparser
import os
import json
import requests
import re
import time
import hashlib

cwd = os.path.split(os.path.realpath(__file__))[0]
config = configparser.ConfigParser()
config.read(os.path.join(cwd, "../conf.ini"))   # 注意这里必须是绝对路径
log = os.path.join(cwd, "../logs/filter.log")

ruleapi = config.get("cmdb", "ruleapi")
sk=config.get("ack", "sk")
acklink=config.get("ack", "acklink")
acktype=config.get("ack", "acktype")
ackinfo=config.get("ack", "ackinfo")

def filterlog(status,to_list, subject):
	curdate = time.strftime('%F %X')
	with open(log, 'a+') as f:
		f.write(curdate + " " + status + " " + to_list + " " + subject + "\n")

def initMsg(msg):
	msg = msg.replace("'", '"')
	msg = json.loads(msg)
	return msg

def getConf(section, option):
	try:
		ret = config.get(section, option)
	except:
		ret = ""
	return(ret)

def genAckLink(eventid):
	try:
		Md5 = hashlib.md5()
		Sha1 = hashlib.sha1()
		Md5.update((eventid + sk).encode('utf-8'))
		Sha1.update(Md5.hexdigest().encode('utf-8'))
		sign = Sha1.hexdigest()
		return(acklink + "?type=" + acktype + "&eventids=" + eventid + "&sign=" + sign)
	except:
		return("")

def checkThreshold(key, Type, name, value):
	value = value.split('/')
	try:
		if(len(value) == 2):
			value = float(value[0])/float(value[1])
		else:
			value = float(value[0])
	except:
		value = 0.0

	url = ruleapi + "?type=" + Type + "&value=" + name
	r = requests.get(url)
	try:
		rule = r.json()
		org_id = rule['org_id']
	except:
		return None,True
	key = re.sub('\[.*?\]', '',key)
	key = getConf('threshold', key)

	# 没有定义规则的直接返回True(即达到阈值)
	if not rule['rules'] or key not in rule['rules'].keys():
		return org_id,True
	threshold = float(rule['rules'][key]['threshold'])
	if value > threshold:
		return org_id,True
	else:
		return org_id,False

def ack(eventid):
	ackurl = genAckLink(eventid)
	ackurl = re.sub('index.php','ack.php', ackurl)
	ackurl = ackurl + '&user=zabbix-alert&note=custom_threshold_filtered&deal=silence'
	try:
		requests.get(ackurl)
	except:
		pass

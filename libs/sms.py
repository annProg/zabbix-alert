#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: sms.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-07-05 14:59:40
############################

import configparser
import requests
import json
import time

#解析配置文件
config = configparser.ConfigParser()
config.read("conf.ini")   # 注意这里必须是绝对路径

sms_addr=config.get("sms", "addr")
sms_user=config.get("sms", "user_name")
sms_pass=config.get("sms", "pass_md5")

log="logs/sms.log"

def sendlog(status, msgid,  to_list, subject):
	curdate = time.strftime('%F %X')
	subject = subject.replace("\n", "#")
	with open(log, 'a+') as f:
		f.write(curdate + " " + status + " " + msgid + " " + to_list + " " + subject + "\n")

def send_sms(to, msg):
	headers = {"accept":"application/json", "content-type":"application/json;charset=utf-8"}
	data = {"usr":sms_user, "pwd":sms_pass, "to":to, "msg":msg}
	r = requests.post(sms_addr, headers=headers, data=json.dumps(data))
	ret = r.json()
	status = ret['statuscode']
	msgid = ret['messageid']
	sendlog(status, msgid, to, msg)
	return ret

if __name__ == '__main__':
	to="1111"
	msg="短信发送测试"
	ret = send_sms(to,msg)


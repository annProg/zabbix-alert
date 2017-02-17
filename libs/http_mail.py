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
import sys

#解析配置文件
config = configparser.ConfigParser()
config.read("conf.ini")   # 注意这里必须是绝对路径

mail_api=config.get("http_mail", "mail_api")
mail_from=config.get("http_mail", "from")
cc_list=config.get("send", "mailcc_list")

log="logs/http_mail.log"

def sendlog(status, to_list, subject):
	curdate = time.strftime('%F %X')
	with open(log, 'a+') as f:
		f.write(curdate + " " + status + " " + to_list + " " + subject + "\n")

def http_send_mail(to, sub, content, mail_format="html", mail_from=mail_from):
	#headers = {"content-type":"application/x-www-form-urlencoded;charset=utf-8"}
	data = {"tos":to, "cc":cc_list, "subject":sub, "content":content, "from":mail_from, "format":mail_format}
	r = requests.post(mail_api, data=data)
	ret = r.json()
	status = str(ret['status']) + "-" + ret['msg']
	sendlog(status, to, sub)
	return ret

if __name__ == '__main__':
	to=sys.argv[1]
	msg="http_mail测试"
	ret = http_send_mail(to,"http_mail测试", msg)
	print(ret)


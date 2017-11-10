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
from requests_toolbelt import MultipartEncoder
import requests
import json
import time
import sys

#解析配置文件
config = configparser.ConfigParser()
config.read("conf.ini")   # 注意这里必须是绝对路径

mail_api=config.get("http_mail", "mail_attach")
mail_from=config.get("http_mail", "from")

log="logs/http_mail.log"

def sendlog(status, to_list, subject):
	curdate = time.strftime('%F %X')
	with open(log, 'a+') as f:
		f.write(curdate + " " + status + " " + to_list + " " + subject + "\n")

def http_send_attachmail(to, cc, sub, content, filelist=[], mail_format="html", mail_from=mail_from):
	attachNum = str(len(filelist))
	attachs = {}
	i = 1
	for attach in filelist:
		idx = 'attach' + str(i)
		attachs[idx] = (attach, open(attach, "rb"))
		i+=1
	
	fields = {"tos":to, "cc":cc, "subject":sub, "content":content, "from":mail_from, "format":mail_format, "attachNum":attachNum}
	fields = dict(fields, **attachs)
	m = MultipartEncoder(fields)
	headers = {"content-type":m.content_type}
	r = requests.post(mail_api, data=m, headers=headers)
	ret = r.json()
	status = str(ret['status']) + "-" + ret['msg']
	sendlog(status, to, sub)
	return ret

if __name__ == '__main__':
	to=sys.argv[1]
	msg="http_mail测试<img src=\"cid:file1.png\"/>"
	ret = http_send_attachmail(to,"http_mail测试", msg, ["file1.png"])
	print(ret)


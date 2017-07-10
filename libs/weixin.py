#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: weixin.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-07-06 16:16:41
############################

import requests
import configparser
import json
import time

#解析配置文件
cfg = "conf.ini"
config = configparser.ConfigParser()
config.read(cfg)   # 注意这里必须是绝对路径

corpid=config.get("weixin", "corpid")
secret=config.get("weixin", "secret")
token=config.get("weixin", "token")

def getToken():
	gettoken_api = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + secret
	r = requests.get(gettoken_api)
	token = r.json()['access_token']
	config.set("weixin", "token", token)
	config.write(open(cfg, "w"))
	return(token)

def sendlog(status, to_list, subject):
	log="logs/weixin.log"
	curdate = time.strftime('%F %X')
	subject = subject.replace("\n", "#")
	with open(log, 'a+') as f:
		f.write(curdate + " " + status + " " + to_list + " " + subject + "\n")

def try_send(to, msg, agentid=1, token=token):
	sendmsg_api = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
	data = {"touser":to, "msgtype":"text", "agentid":agentid, "text":{"content":msg}}
	jsondata = json.dumps(data, ensure_ascii=False)
	r = requests.post(sendmsg_api, data=jsondata.encode('utf-8'))
	ret = r.json()
	return(ret)

def send_weixin(to, msg, agentid=1):
	ret = try_send(to, msg, agentid)
	if ret['errcode'] != 0:
		token = getToken()
		ret = try_send(to, msg, agentid, token)
		sendlog(ret['errmsg'],to, msg)
		return(ret)
	sendlog(ret['errmsg'],to, msg)
	return(ret)

if __name__ == '__main__':
	to="abc|def"
	msg="微信发送测试"
	ret = send_weixin(to,msg)
	print(ret)

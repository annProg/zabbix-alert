#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: common.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-06-27 14:59:10
############################

import json
import sys
import os
import os.path
import requests
from libs.db import init_DB
from libs.mail import send_mail
from libs.http_attachmail import http_send_attachmail
from libs.sms import send_sms
from libs.weixin import send_weixin
from libs.rand import GenPassword
from json2table import convert
import configparser
import re
from PIL import Image
from io import BytesIO
import hashlib
from influxdb import InfluxDBClient
import copy


#解析配置文件
config = configparser.ConfigParser()
config.read("conf.ini")   # 注意这里必须是绝对路径

email_default = config.get("send", "mailto_list")
weixin_default = config.get("send", "weixin_list")
sms_default = config.get("send", "sms_list")
cmdbapi = config.get("cmdb", "api")
dashhome = config.get("dashboard", "dashhome")
home = config.get("dashboard", "home")
team = config.get("dashboard", "team")
dir_threshold = config.get("http_mail", "dir_threshold")
sk=config.get("ack", "sk")
acklink=config.get("ack", "acklink")
acktype=config.get("ack", "acktype")
ackinfo=config.get("ack", "ackinfo")
mail_suffix=config.get("send", "mail_suffix")
name_replace=config.get("misc", "name_replace")

def getConf(section, option):
	try:
		ret = config.get(section, option)
	except:
		ret = ""
	return(ret)

iptype = getConf("cmdb", "iptype").split(",")

def getContact(citype, civalue, rankdir="TB", ips=""):
	values = civalue
	direction = "down"
	if citype in iptype:
		citype = "ip"
		values = ips
		va_len = len(ips.split(","))
		if va_len > 1:
			direction = "both"
	url = cmdbapi + "?type=" + citype + "&value=" + values + "&rankdir=" + rankdir + "&direction=" + direction
	r = requests.get(url)
	contact = {}
	contact['email'] = []
	contact['mobile'] = []

	try:
		apidata = r.json()
		persons = apidata['objects']
		if "imgurl" in apidata:
			imgurl = apidata['imgurl']
	except:
		contact['email'].append(email_default)
		contact['mobile'].append(sms_default)
		imgurl = ""
		return(contact, imgurl)

	if not persons:
		contact['email'].append(email_default)
		# 短信频率及数量限制，仅在citype不为app且无人接收时发给默认处理人
		if citype != "app":
			contact['mobile'].append(sms_default)
	else:
		for k,v in persons.items():
			v_email = v['fields']['email']
			v_mobile = v['fields']['phone']
			if v_email:
				contact['email'].append(v['fields']['email'])
			if v_mobile:
				contact['mobile'].append(v['fields']['phone'])
	return(contact, imgurl)

def genAckLink(msg):
	try:
		Md5 = hashlib.md5()
		Sha1 = hashlib.sha1()
		Md5.update((msg['eventid'] + sk).encode('utf-8'))
		Sha1.update(Md5.hexdigest().encode('utf-8'))
		sign = Sha1.hexdigest()
		return(acklink + "?type=" + acktype + "&eventids=" + msg['eventid'] + "&sign=" + sign)
	except:
		return("")

def Http_Mail(emails, msg, filelist):
	sub = status + ": " + msg['主题']
	newmsg = copy.deepcopy(msg)
	linkimg = newmsg['关联图']
	itemvalue = {}
	itemvalue['数据'] = newmsg['数据']
	del newmsg['关联图']
	del newmsg['数据']

	pre = "详情请登录 <a href=\"" + dashhome + "\">" + dashhome + "</a><br/><hr>"
	if status != "OK":
		ackurl = genAckLink(newmsg)
		if ackurl != "":
			pre = '<p><a href="' + ackurl + '">' + ackinfo + '</a></p>' + pre
	try:
		del newmsg['eventid']
	except:
		pass

	build_direction = "LEFT_TO_RIGHT"
	table_attributes = {"style": "width:100%", "border": "1"}
	#table_attributes = {"style": "width:100%;border:1px solid #000;", "border": "1"}
	html = convert(newmsg, build_direction=build_direction, table_attributes=table_attributes)
	html_data = convert(itemvalue, build_direction=build_direction, table_attributes=table_attributes)
	html = "<h3>基本信息</h3>" + html + "<br><h3>监控项数据</h3>" + html_data

	link = "<p><h3>报警对象影响范围图</h3></p><p>" + linkimg + "</p>"
	suffix = "<hr><br>" + link + "<br><hr><b>" + team + "</b><br>主页: <a href=\"" + home + "\">" + home + "<br><hr><br>"
	html = pre + html + suffix
	http_send_attachmail(emails, sub, html, filelist)

def Mail(emails, msg):
	sub = status + ": " + msg['主题']

	build_direction = "LEFT_TO_RIGHT"
	table_attributes = {"style": "width:100%", "border": "1"}
	#table_attributes = {"style": "width:100%;border:1px solid #000;", "border": "1"}
	html = convert(msg, build_direction=build_direction, table_attributes=table_attributes)
	pre = "详情请登录 <a href=\"" + dashhome + "\">" + dashhome + "</a><br/><hr>"
	suffix = "<hr><br><br><hr><b>智能云平台 运维组</b><br>主页: <a href=\"" + home + "\">" + home + "<br><hr><br>"
	html = pre + html + suffix
	send_mail(emails, sub, html, 1)

def SMS(mobiles, msg):
	values = []
	for item in msg['数据']:
		values.append(item['Value'])
	value_str = "|".join(values)
	content = "状态: " + status + "\n" + \
		"主题: " + msg['主题'] + "\n" + \
		"范围: " + msg['名称'] + "\n" + \
		"Values: " + value_str + "\n" + \
		"故障时间: " + msg['数据'][0]['故障时间'] + "\n" + \
		"故障时长: " + msg['数据'][0]['故障时长'].split(">")[1].split("<")[0] + "\n" + \
		"详情请查看邮件"
	send_sms(mobiles, content)

def Weixin(weixin, msg):
	values = []
	for item in msg['数据']:
		values.append(item['Value'])
	value_str = "|".join(values)[0:1500]  # 防止超出微信内容长度限制(2k)，超限会发送失败
	content = "状态: " + status + "\n" + \
			"主题: " + msg['主题'] + "\n" + \
			"范围: " + msg['名称'] + "\n" + \
			"Values: " + value_str + "\n" + \
			"故障时间: " + msg['数据'][0]['故障时间'] + "\n" + \
			"故障时长: " + msg['数据'][0]['故障时长'].split(">")[1].split("<")[0] + "\n" + \
			"详情请查看邮件"
	return(send_weixin(weixin, content))

def killOneLineMsg(msg):
	data = msg['数据']
	if len(data) == 1:
		item = data[0]
		newitem = {}
		for k,v in item.items():
			newitem[k] = "<center>" + k + "</center>"
		msg['数据'].append(newitem)
	return(msg)

def convertDuration(duration):
	p = re.compile(r'd|h')
	news = re.sub(p, '#', re.sub('m| ', '', duration)).split("#")[::-1]
	news.extend(["0","0"])
	news = news[0:3:1]
	return(float(news[0]) + float(news[1])*60 + float(news[2])*1440)

def influxDB(contact, msg, sendtype="mail"):
	client = InfluxDBClient(config.get("influxdb", "server"), config.get("influxdb", "port"), \
			config.get("influxdb","user"), config.get("influxdb", "passwd"), config.get("influxdb","database"))
	client.create_database(config.get("influxdb", "database"))
	
	duration = msg["数据"][0]["故障时长"].split(">")[1].split("<")[0]
	duration = convertDuration(duration)
	if "IP" in msg:
		name = msg['IP'].split("\n")
	else:
		name = msg['名称'].split("\n")

	ownerlist = sorted(contact.replace(mail_suffix, "").split(","))
	owner = ",".join(ownerlist)

	for item in name:
		json_body = [{
					"measurement":"alert",
					"tags": {
						"sendtype":sendtype,
						"subject":msg['主题'],
						"owner":owner,
						"alerttype":msg['类型'],
						"status":status,
						"name":item,
						"level":msg['严重性']
						},
					"fields": {
							"value": 1,
							"duration":duration,
						}
					}]
		client.write_points(json_body)

	# 以个人为单位统计报警量
	for item in ownerlist:
		json_body = [{"measurement":"ownercount","tags":{"owner":item,"sendtype":sendtype},"fields":{"value":1}}]
		client.write_points(json_body)
		
def sendAlert(contact,msg, filelist=[]):
	emails = ",".join(list(set(",".join(contact['email']).split(","))))
	# mobiles 必须去重，公司的短信接口，同一次调用如果有相同的手机号，会返回000018(1分钟频率限制)
	mobiles = ",".join(list(set(",".join(contact['mobile']).split(","))))
	weixin = emails.replace(mail_suffix,"").replace(",","|")
	weixin = re.sub('\d', '', weixin)
	severity = msg['严重性']

	msg['名称'] = msg['名称'].replace("\n", "<br>")
	weixin_exclue = ['Notice']
	if severity not in weixin_exclue:
		weret = Weixin(weixin, msg)
		influxDB(emails, msg, "weixin")
		if weret['errcode'] != 0:
			msg['附加信息2'] = "微信发送失败，请关注公众号"

	sms_severity = ['High', 'Disaster', 'CRITICAL']
	if severity in sms_severity:
		if mobiles:
			SMS(mobiles, msg)
			influxDB(emails, msg, "sms")
		else:
			msg['附加信息'] = "短信号码为空！请登录CMDB设置手机号，以便接收短信报警"
	Http_Mail(emails, msg, filelist)
	influxDB(emails, msg, 'mail')

def getDashBoard(msg):
	if msg['类型'] == "app":
		dash_url = config.get('dashboard', 'app')
		detail_url = dash_url
	elif msg['类型'] == "url":
		dashs = []
		urls = msg['名称'].split('\n')
		dash_url = config.get('dashboard', 'url')
		for url in urls:
			detail_url = dash_url + "?var-monit_node=" + msg['监控点'] + \
				"&var-app=" + msg['APP'] + "&var-url=" + url
			dashs.append("<a href=\"" + detail_url + "\">" + dash_url + "</a>")
		return('<br>'.join(dashs))
	else:
		dash_url = config.get('dashboard', 'default')
		detail_url = dash_url
	data = "<a href=\"" + detail_url + "\">" + dash_url + "</a>"
	return(data)

def getImg(imgurl):
	filelist = []
	r = requests.get(imgurl)
	imgtype = r.headers["content-type"].split(";")[0].split("/")[1]
	imgname = "alert_img_" + GenPassword(16) + "." + imgtype
	imgpath = "/tmp/" + imgname
	if r.status_code == requests.codes.ok:
		i = Image.open(BytesIO(r.content))
		i.save(imgpath)

	filelist.append(imgpath)
	return(imgpath, filelist)

if __name__ == '__main__':
	#print(getContact("app", sys.argv[1]))
	msg = init_DB(sys.argv[1])
	#msg = killOneLineMsg(msg)
	#print(json.dumps(msg))
	ci_len = len(msg['名称'].split(","))
	rankdir = "TB"
	if ci_len > int(dir_threshold):
		rankdir = "LR"
	if "IP" in msg:
		contact, imgurl = getContact(msg['类型'], msg['名称'], rankdir, msg['IP'])
		msg['IP'] = msg['IP'].replace(",","\n")
	else:
		contact, imgurl = getContact(msg['类型'], msg['名称'], rankdir)
	if msg['类型'] == 'url':
		msg['名称'] = msg['名称'].replace(",","\n")
	else:
		msg['名称'] = msg['名称'].replace(name_replace,"").replace(",","\n")
	status = msg['状态'].split(">")[1].split("<")[0]
	msg['监控图表'] = getDashBoard(msg)
	if imgurl != "":
		imgname, filelist = getImg(imgurl)
		msg['关联图'] = '<p><img class="aligncenter" src="cid:' + imgname + '" alt="对象影响图示" /></p>'
	else:
		filelist = []

	sendAlert(contact, msg, filelist)

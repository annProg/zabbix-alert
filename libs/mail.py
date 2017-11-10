#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: mail.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2015-10-19 16:58:05
############################

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
import configparser
import re

#解析配置文件
config = configparser.ConfigParser()
config.read("conf.ini")   # 注意这里必须是绝对路径

mail_host=config.get("mailserver", "server")
mail_user=config.get("mailserver", "user")
mail_pass=config.get("mailserver", "passwd")
mail_postfix=config.get("mailserver", "postfix")
mail_suffix=config.get("send", "mail_suffix")


log="logs/mail.log"

def maillog(status, mailto_list, subject):
	curdate = time.strftime('%F %X')
	with open(log, 'a+') as f:
		f.write(curdate + " " + status + " " + ",".join(mailto_list) + " " + subject + "\n")

def addImg(src, imgid):
	fp = open(src, 'rb')  
	try:
		msgImage = MIMEImage(fp.read())
		fp.close()  
		msgImage.add_header('Content-ID', imgid)  
		return msgImage
	except:
		return(False)

#定义send_mail函数
def send_mail(to_list, cc,  sub, content, html=1, imgs=""):
	'''
	to_list:发送列表，逗号分隔
	sub:主题
	content:内容
	send_mail("admin@qq.com","sub","content")
	'''

	address=mail_user+"<"+mail_user+"@"+mail_postfix+">"
	
	msg = MIMEMultipart('mixed')
	if html == 0:
		part = MIMEText(content, 'plain', 'utf-8')
	else:
		part = MIMEText(content, 'html', 'utf-8')
	msg['Subject'] = sub
	msg['From'] = address

	msg.attach(part)
	
	# 图片
	if imgs:
		for img in imgs.split(","):
			imgid = img.split("/")[-1]
			if addImg(img, imgid):
				msg.attach(addImg(img, imgid))
			else:
				continue

	to_list = to_list.split(",")
	msg['To'] =";".join(to_list)
	msg['Cc'] =";".join(cc)
	toaddrs = to_list + cc #抄送人也要加入到sendmail函数的收件人参数中，否则无法收到
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		#s.login(mail_user,mail_pass)
		s.sendmail(address, toaddrs, msg.as_string())
		s.close()
		
		maillog("success", toaddrs, sub)
		return True
	except Exception as e:
		print(str(e))
		maillog(str(e), toaddrs, sub)
		return False

if __name__ == '__main__':
	sub = sys.argv[2].replace("\n", "")
	sub = sub.replace("\r\n", "")
	regex = re.compile(r'DETAIL:.*$')
	sub = regex.sub("DETAIL:", sub)

	to_list = sys.argv[1]
	to_list = to_list.split(",")
	new_list = []
	for to in to_list:
		if "@" in to:
			new_list.append(to)
		else:
			to = to + mail_suffix
			new_list.append(to)
	new_list = ",".join(new_list)

	# 当msg参数以path:开头时，从文本读取邮件内容。可以处理邮件内容过长超过Linux系统参数长度的情况
	if re.match("^path:", sys.argv[3]):
		path = sys.argv[3].split(':')[1]
		try:
			msg = open(path).read()
		except:
			msg = sys.argv[3]
	else:
		msg = sys.argv[3]
	
	if len(sys.argv) == 6:
		imgs = sys.argv[5]
	else:
		imgs = ""

	if len(sys.argv) == 4:
		print(new_list)
		send_mail(new_list, sub, msg, 0)
	else:
		print(new_list)
		send_mail(new_list, sub, msg, 1, imgs)

	#send_mail(mailto_list, "test", "this is a test message")


#!/usr/bin/python3

###########################
#  name: k2zabbix.py
#  usage: kapacitor报警调用zabbix-alert脚本处理
#  date: 2016-08-18
###########################

import sys
import os
import json
from html.parser import HTMLParser
import datetime
import requests
import re

zabbix_alert = "/opt/kapacitor/zabbix-alert/reduce.py"
p = HTMLParser()

def initFile(tmpfile):
	with open(tmpfile,'r') as f:
		data = json.load(f)
	return(data)
	
def initStdin():
	data = json.loads(sys.stdin.readline())
	return(data)

def time0to8(timestr):
	time_0 = datetime.datetime.strptime(timestr,"%Y-%m-%dT%H:%M:%SZ")
	time_8 = time_0 + datetime.timedelta(hours=8)
	DATETIME = str(time_8.strftime('%Y-%m-%d %H:%M:%S'))
	return(DATETIME)

def downtime(timestr,duration):
	now = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
	down = now - datetime.timedelta(seconds=duration)
	return(str(down.strftime('%Y-%m-%d %H:%M:%S')))

def second_friendly(second):
	days = int(second/(60*60*24))
	hours = int(second/(60*60)) - days * 24
	minutes = second/60 - days * 24 * 60 - hours * 60
	
	d_str,h_str,m_str = "d","h","m"
	if days == 0:
		days,d_str = "",""
	if hours == 0:
		hours,h_str = "",""
	if minutes == 0:
		minutes,m_str = 0,""
	return(str(days) + d_str + str(hours) + h_str + str("%.2f"%minutes) + m_str)

def urlstatus(url):
	cmdbapi = "http://cmdb.opt.cn/api/public.php?type=url&value=" + url
	r = requests.get(cmdbapi)
	data = r.json()['objects']
	if not data:
		return(False)
	return(True)
	
def setmatchok(tags):
	kapacitorapi = "http://localhost:9092/kapacitor/v1/write?db=telegraf&rp=default"
	data = "url_monitor,app=" + tags['app'] + ",url=" + tags['url'] + ",monitor_node=" + tags['monitor_node'] + \
		" code_match=1,data_match=1"
	for i in range(1,3):
		r = requests.post(kapacitorapi, data=data)
	return(r.headers)
	

def main(data):
	details = json.loads(p.unescape(data['details']))
	alert = {}
	duration = data['duration']/1000000000
	alert['age'] = second_friendly(duration)
	alert['datetime'] = time0to8(details['Time'])
	alert['downtime'] = downtime(alert['datetime'],duration)
	alert['name'] = data['id']
	alert['hostgroup'] = details['Name']
	alert['severity'] = details['Level']
	alert['cmdbid'] = details['Tags']['cmdbid']

	alert['app'] = details['Tags']['app']
	try:
		alert['cmdbid'] = details['Tags']['cmdbid']
	except:
		alert['cmdbid'] = "0"
	alert['url'] = details['Tags']['url']
	alert['monitor_node'] = details['Tags']['monitor_node']
	try:
		alert['code'] = details['Fields']['http_code.last']
	except:
		alert['code'] = "UNKNOWN"
	
	if not urlstatus(alert['url']):
		print(setmatchok(alert))
	
	try:
		alert['msg'] = details['Fields']['msg.last']
	except:
		alert['msg'] = "UNKNOWN"

	if alert['severity'] != "OK":
		alert['status'] = "PROBLEM"
	else:
		alert['status'] = "OK"
	try:
		alert['rt'] = str("%.3f"%details['Fields']['response_time.last'])
	except:
		alert['rt'] = "UNKNOWN"

	if re.search(r'^HTTP_CODE:.*', alert['name']):
		alert['value'] = "CodeRequired:" + details['Fields']['require_code.last'] + "<br>CodeReal:" + str(alert['code'])
	elif re.search(r'^RESPONSE_DATA:.*', alert['name']):
		alert['value'] = "DataRequired:" + details['Fields']['require_str.last'] + "<br>DataReal:" + alert['msg']
	else:
		alert['value'] = "TimeRequired:" + details['Fields']['require_time.last'] + "<br>TimeReal:" + alert['rt']

	argstr = json.dumps(alert)

	print(argstr)
	output = os.popen(zabbix_alert + " 1 2 '" + argstr + "'")

if __name__ == '__main__':
	if sys.argv[1] == "test":
		data = initFile(sys.argv[2])
	if sys.argv[1] == "product":
		data = initStdin()
	main(data)	

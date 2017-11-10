#!/bin/bash

############################
# Usage:
# File Name: cron.sh
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-07-01 09:48:41
############################

basedir=$(cd `dirname $0`; pwd)
now=`date +%s`

cd $basedir
ps aux |grep "./api.py" |grep -v "grep" || ./api.py > logs/api.log 2>&1 &

cd new
for id in `ls`;do
	severity=`echo $id |cut -f1 -d'.' |awk -F '_' '{print $NF}'`
	trigger_status=`echo $id |cut -f2 -d'.'`
	case $severity in
		LoadWarn) threshold="180";;
		Information) threshold="480";;  # 此处值不应过大，需要参考step的间隔，过大可能导致告警一直达不到threshold
		Warning) threshold="60";;
		Average) threshold="50";;
		High) threshold="40";;
		*) threshold="40";;
	esac

	[ "$trigger_status"x = "OK"x ] && threshold="180"

	mod=`stat $id -c %Y`
	((interval=now-mod))
	[ $interval -gt $threshold ] && mv $id ../queue

	# 超过30个数据项，直接发送, 防止某些报警连续发送一直达不到阈值
	count=`cat $id |jq . |grep "name" |wc -l`;
	[ $count -gt 30 ] && mv $id ../queue	
done


cd ..

for id in `ls queue/`;do
	./alert.py "queue/$id"
	[ $? -eq 0 ] && mv queue/$id old || mv queue/$id failed
	#[ $? -eq 0 ] && mv queue/$id old || echo "$id 发送失败" | mail -s "$id 发送失败" xxx@xx.com
done

#!/bin/bash

############################
# Usage:
# File Name: init.sh
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2016-07-01 14:58:30
############################

basedir=$(cd `dirname $0`; pwd)
cd $basedir

if [ "$1"x = "init"x ];then
	for id in `grep "folder_" conf.ini|awk '{print $3}'`;do
		[ ! -d $id ] && mkdir $id
	done
elif [ "$1"x = "cron"x ];then
	cat >>/etc/crontab<<EOF
# zabbix-alert定时发告警
* * * * * root $basedir/cron.sh
* * * * * root sleep 15;$basedir/cron.sh
* * * * * root sleep 30;$basedir/cron.sh
* * * * * root sleep 45;$basedir/cron.sh
EOF
elif [ "$1"x = "monit"x ];then
	echo "queue: `ls queue |wc -l`"
	echo "new: `ls new |wc -l`"
fi

chown -R zabbix.zabbix $basedir

# Zabbix告警脚本
支持简单压缩合并

配置动作,默认信息

```
{'date':'{DATE}', 'time':'{TIME}', 'itemid':'{ITEM.ID}', 'actionid':'{ACTION.ID}', 'downdate':'{EVENT.DATE}', 'downtime':'{EVENT.TIME}', 'age':'{EVENT.AGE}', 'ip':'{HOST.CONN1}', 'triggerid':'{TRIGGER.ID}', 'name':'{TRIGGER.NAME}', 'status':'{TRIGGER.STATUS}', 'severity':'{TRIGGER.SEVERITY}', 'url':'{TRIGGER.URL}', 'itemname':'{ITEM.NAME1}', 'itemname2':'{ITEM.NAME2}', 'hostname':'{HOST.HOST1}', 'itemkey':'{ITEM.KEY1}', 'itemkey2':'{ITEM.KEY2}','itemvalue':'{ITEM.VALUE1}', 'itemvalue2':'{ITEM.VALUE2}', 'eventid':'{EVENT.ID}','hostgroup':'{TRIGGER.HOSTGROUP.NAME}'}
```

恢复信息

```
{'date':'{DATE}', 'time':'{TIME}', 'itemid':'{ITEM.ID}', 'actionid':'{ACTION.ID}', 'downdate':'{EVENT.DATE}', 'downtime':'{EVENT.TIME}', 'age':'{EVENT.AGE}', 'ip':'{HOST.CONN1}', 'triggerid':'{TRIGGER.ID}', 'name':'{TRIGGER.NAME}', 'status':'{TRIGGER.STATUS}', 'severity':'{TRIGGER.SEVERITY}', 'url':'{TRIGGER.URL}', 'itemname':'{ITEM.NAME1}', 'itemname2':'{ITEM.NAME2}', 'hostname':'{HOST.HOST1}', 'itemkey':'{ITEM.KEY1}', 'itemkey2':'{ITEM.KEY2}','itemvalue':'{ITEM.VALUE1}', 'itemvalue2':'{ITEM.VALUE2}', 'eventid':'{EVENT.ID}','hostgroup':'{TRIGGER.HOSTGROUP.NAME}','update':'{EVENT.RECOVERY.DATE}', 'uptime':'{EVENT.RECOVERY.TIME}'}
```

## HTTP MAIL
使用 <https://github.com/iambocai/mailer> 在多台机器上搭建并使用Nginx做负载均衡，避免单台机器发送频率过快被对方服务器限制。

如使用本地smtp，建议使用postfix搭建。sendmail会出现 `unencrypted connection` 错误。原因尚未调查。

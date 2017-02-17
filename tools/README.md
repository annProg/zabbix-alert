## k2zabbix.py
在tickscript中调用此脚本，转换成zabbix-alert能够处理的格式。

tickscript实例，
```
var win = 3m
var origin = stream
	|from()
		.database('telegraf')
		.retentionPolicy('default')
		.measurement('url_monitor')
		.groupBy('monitor_node','app','url', 'cmdbid')
	|window()
		.period(win)
		.every(10s)

var code_match = origin
	|mean('code_match')

var http_code = origin
	|last('http_code')

var require_code = origin
	|last('require_code')

code_match
	|join(http_code, require_code)
		.as('code_match', 'http_code', 'require_code')
		.tolerance(5s)

	|alert()
		.id('HTTP_CODE:{{ index .Tags "cmdbid" }}.{{ index .Tags "url" }}')
		.message('')
		.crit(lambda: "code_match.mean" < 0.4)
		.critReset(lambda: "code_match.mean" == 1)
		.stateChangesOnly(30m)
		.log('/tmp/alerts.log')
		.exec('/opt/kapacitor/tools/k2zabbix.py', 'product')
		.alerta()
			.resource('{{ index .Tags "cmdbid" }}.{{ index .Tags "monitor_node" }}:{{ index .Tags "app" }}')
			.event('状态码异常: {{ index .Tags "url" }}')
			.environment('Production')
			.group('{{ index .Tags "cmdbid" }}.{{ index .Tags "monitor_node" }}:{{ index .Tags "app" }}')
			.value('{{ index .Fields "http_code.last" }}')
```

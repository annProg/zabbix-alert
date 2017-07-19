#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: api.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2017-07-19 15:48:34
############################

from flask import Flask, request
from flask_restful import Api, Resource
import configparser
import json
import os

#解析配置文件
config = configparser.ConfigParser()
config.read("conf.ini")   # 注意这里必须是绝对路径

host = config.get("api", "host")
port = config.getint("api", "port")

app = Flask(__name__)
api = Api(app)

class Reduce(Resource):
	def post(self):
		if request.json:
			arg = json.dumps(request.json)
			r = os.popen("python3 reduce.py 1 2 '%s'" %(arg))
			ret = r.read().strip('\n')
			if not ret:
				return {'code':0, 'msg':'succ'},200
			else:
				print(ret)
		return {'code':100, 'msg':'bad request'}, 400

if __name__ == '__main__':
	api.add_resource(Reduce, '/alert')
	app.run(host=host,port=port,debug=True)

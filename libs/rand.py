#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: rand.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2015-10-24 15:26:08
############################

'''
简短地生成随机密码，包括大小写字母、数字，可以指定密码长度
'''
#生成随机密码
from random import choice
import string
import sys

#python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters

def GenPassword(length=14,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def GenDigit(length=4,chars=string.digits):
    return ''.join([choice(chars) for i in range(length)])

if __name__=="__main__":
    #生成10个随机密码    
    passlen = int(sys.argv[1])
    print(GenPassword(passlen).lower())

#!/usr/bin/env python
# coding:utf8
import os
import sys


def sed(old,new):
    list = []
    f1 = open('{}'.format(filename),'r')
    lines = f1.readlines()
    for line in lines:
        if old in line:
            line = line.replace(old,new)
            list.append(line)
	    else:
	        list.append(line)
    f2 = open('{}'.format(filename),'w')
    for i in list:
        f2.write(i)

#try:
filename = sys.argv[1]
old = sys.argv[2]
new = sys.argv[3]
sed(old,new)
#except:
#    print('有异常发生')

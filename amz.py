#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 13:32:41
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-13 14:37:44

# from amz_utils import *
import amz_utils
import json

from collections import deque

def log(line):
    amz_utils.log(line)

def elog(line):
    amz_utils.elog(line)

def execute(cmd):
    return amz_utils.execute(cmd)

def search(name):
    out, err = execute("aws ec2 describe-images --filters 'Name=name,Values={0}'".format(name))
    if err:
        elog(err)
    result = json.loads(out)
    log("Number of results: {0}".format(len(result["Images"])))
    return out

def test():
    res = search("ubuntu")

if __name__ == '__main__':

    amz_utils.DEBUG = True 
    test()





















#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 13:32:41
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-13 20:38:51

import amz_utils
import json
import ConfigParser
import sys

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

# Take an image-id as value and try to run this instance by defualt settings.
# If -d is specified, awz will ask for more detailed information about running this new instance.
# If -a is specified, an instances-alias is required for referencing this new instance.
def run_instances(imageId, alias, isDetailed):

    sgroup = "sg-a64e57c1"
    count = "1"
    ins_type = "t2.micro"
    key_name = "yangKey"

    if isDetailed:
        temp = raw_input("> Enter security-group-ids (" + sgroup + "):\n> ")
        if temp:
            sgroup = temp
        temp = raw_input("> Enter number of instances (" + count + "):\n> ")
        if temp:
            count = temp
        temp = raw_input("> Enter instance type (" + ins_type + "):\n> ")
        if temp:
            ins_type = temp
        temp = raw_input("> Enter key name (" + key_name + "):\n> ")
        if temp:
            key_name = temp 

    out,err = execute("aws ec2 run-instances --image-id {0} --security-group-ids {1} --count {2} --instance-type {3} --key-name {4}".format(imageId, sgroup, count, ins_type, key_name))

    if err:
        elog(err)

    try:
        f = open("/Volumes/YangFlashCard/projects/amz/instances/{0}".format(alias), 'w')
        f.write(out)
        f.close()
    except IOError, err:
        elog(err)

def stop_instances(ids):
    pass

def teminate_instances(ids):
    pass


def test(path):
    parser = ConfigParser.loads(path)
    parser.remove("leet")
    parser.save()

if __name__ == '__main__':

    amz_utils.DEBUG = True 
    run_instances("ami-0531bf65", "foo", True)

    # test(sys.argv[1])





















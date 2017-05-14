#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 13:32:41
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-14 16:56:20

import amz_utils
import json
import ConfigParser
import TableParser
import sys

from collections import deque

CONFIG_PATH = "/Users/yang/.ssh/config"
IDENTITY_FILE = "/Users/yang/.ssh/aws-keys/yangKey.pem"
TABLE_PATH = "/Volumes/YangFlashCard/projects/amz/instances/table/table.json"
INFO_PATH = "/Volumes/YangFlashCard/projects/amz/instances/info/"

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
def run_instances(imageId, alias, isDetailed, userName):

    global CONFIG_PATH
    global IDENTITY_FILE

    # load ~/.ssh/config into memory, context is the objecet containing the parsed config file
    context = ConfigParser.loads(CONFIG_PATH)

    dupHost = context.isAliasDup(alias)
    if dupHost:
        elog("duplicated alias name found: {0}".format(dupHost))

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

    log("command :\naws ec2 run-instances --image-id {0} --security-group-ids {1} --count {2} --instance-type {3} --key-name {4} --query 'Instances[0].InstanceId' --output json".format(imageId, sgroup, count, ins_type, key_name))
    instance_id ,err = execute("aws ec2 run-instances --image-id {0} --security-group-ids {1} --count {2} --instance-type {3} --key-name {4} --query 'Instances[0].InstanceId' --output json".format(imageId, sgroup, count, ins_type, key_name))

    log("aws ec2 describe-instances --instance-id {0} --output json".format(instance_id))
    out, err = execute("aws ec2 describe-instances --instance-id {0} --output json".format(instance_id))

    if err:
        elog(err)

    raw_instance = json.loads(out)["Reservations"][0]["Instances"][0]
    baked_instance = {}
    baked_instance["InstanceId"] = raw_instance["InstanceId"]
    baked_instance["ImageId"] = raw_instance["ImageId"]
    baked_instance["PublicDnsName"] = raw_instance["PublicDnsName"]
    baked_instance["PublicIpAddress"] = raw_instance["PublicIpAddress"]
    baked_instance["KeyName"] = raw_instance["KeyName"]
    baked_instance["InstanceType"] = raw_instance["InstanceType"]
    baked_instance["SecurityGroups"] = raw_instance["SecurityGroups"]
    baked_instance["AvailabilityZone"] = raw_instance["Placement"]["AvailabilityZone"]
    baked_instance["UserName"] = userName
    
    newHost = ConfigParser.Host(alias)
    newHost.put("User", userName)
    newHost.put("HostName", baked_instance["PublicDnsName"])
    newHost.put("IdentityFile", IDENTITY_FILE)
    context.add(newHost)
    context.save()

    try:
        f_info = open("/Volumes/YangFlashCard/projects/amz/instances/info/{0}.json".format(alias), 'w')
        f_info.write(json.dumps(baked_instance, indent=4))
        f_info.close()

        table_content = {}
        with open("/Volumes/YangFlashCard/projects/amz/instances/table/table.json", 'r') as f_table_read:
            json_string = f_table_read.read()
            if json_string:
                table_content = json.loads(json_string)

        with open("/Volumes/YangFlashCard/projects/amz/instances/table/table.json", 'w') as f_table_write:
            table_content[alias] = baked_instance["InstanceId"]
            f_table_write.write(json.dumps(table_content))

    except IOError, err:
        elog(err)

def stop_instances(ids):
    pass

def teminate_instances(instance_names):
    # 1. find instnace_id and alias in table.json
    # 2. get instances infomation from ~/.amz/instances/info
    # 3. remove the corresponding infomation from ~/.ssh/config file
    # 4. remove the corresponding infomation from ~/.amz/instances/info and ~/.amz/instances/table
    # 5. terminate instances
    global TABLE_PATH
    global INFO_PATH

    table = TableParser(TABLE_PATH)
    instance_alias_arr = table.find(instance_names)
    table.remove(instance_alias_arr)
    table.save()

    # config = ConfigParser(CONFIG_PATH)
    # configParser.remove(instance_aliases)
    # configParser.save()
    # execute('aws ec2 terminate-instances --instance-ids')


# instance name can be alias or instance id
# returns instances info as json string 
def displayInstance(instance_names):

    global TABLE_PATH
    global INFO_PATH

    table = TableParser.loads(TABLE_PATH)
    instance_alias_arr = table.find(instance_names)

    try:
        for alias in instance_alias_arr:
            with open(INFO_PATH + alias + ".json", 'r') as ins_info:
                print "\n" + alias + ":\n" + ins_info.read()
    except IOError, err:
        elog(err)

def test():
    # run_instances("ami-0531bf65", "bar", False, "ubuntu")
    displayInstance(["foo", "bar"])

if __name__ == '__main__':

    amz_utils.DEBUG = True 
    test()





















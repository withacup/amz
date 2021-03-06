#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 13:32:41
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-14 21:19:36

import json
import sys
import os.path
import amz_utils
import ConfigParser
import TableParser

from collections import deque

def log(line):

    amz_utils.log(line)

def elog(line, description=None):

    amz_utils.elog(line, description)

def execute(cmd):

    return amz_utils.execute(cmd)

def search(name):

    if len(name) < 1:
        elog("Invalid Option", "Insufficient option")
    # I will only take the first value as input
    name = name[0]

    out, err = execute("aws ec2 describe-images --filters 'Name=name,Values={0}'".format(name))
    if err:
        elog(err)

    result = json.loads(out)
    log("Number of results: {0}".format(len(result["Images"])))
    log(out)

# Take an image-id as value and try to run this instance by defualt settings.
# If -d is specified, awz will ask for more detailed information about running this new instance.
# If -a is specified, an instances-alias is required for referencing this new instance.
def run_instances(options):

    global CONFIG_PATH
    global IDENTITY_FILE
    global TABLE_PATH
    global INFO_PATH

    # default values
    isDetailed = False
    userName = "root"

    if len(options) < 2:
        elog("Invalid Options", "Insufficient values")

    imageId = options.pop(len(options) - 1)
    alias = options.pop(len(options) - 1)

    while len(options) > 0:
        op = options.pop(0)
        if op == "-d" or op == "-detail":
            isDetailed = True
        elif op == "-u" or op == "-user":
            if len(options) == 0:
                elog("Invalid Options", "insufficient values")
            op = options.pop(0)
            userName = op
        else:
            elog("Invalid Option", "Unkown option: " + op)

    # load ~/.ssh/config into memory, context is the object containing the parsed ~/.ssh/config file
    context = ConfigParser.loads(CONFIG_PATH)

    # check if the alias is occupied
    dupHost = context.isAliasDup(alias)
    if dupHost:
        elog("duplicated alias name found: {0}".format(dupHost))

    # default values
    sgroup = "sg-a64e57c1"
    count = "1" # does not support multiple instances yet
    ins_type = "t2.micro"
    key_name = "yangKey"

    if isDetailed:
        temp = raw_input("> Enter security-group-ids (" + sgroup + "):\n> ")
        if temp:
            sgroup = temp
        # temp = raw_input("> Enter number of instances (" + count + "):\n> ")
        # if temp:
        #     count = temp
        temp = raw_input("> Enter instance type (" + ins_type + "):\n> ")
        if temp:
            ins_type = temp
        temp = raw_input("> Enter key name (" + key_name + "):\n> ")
        if temp:
            key_name = temp 

    log("command :\naws ec2 run-instances --image-id {0} --security-group-ids {1} --count {2} --instance-type {3} --key-name {4} --query 'Instances[0].InstanceId' --output json".format(imageId, sgroup, count, ins_type, key_name))
    instance_id ,err = execute("aws ec2 run-instances --image-id {0} --security-group-ids {1} --count {2} --instance-type {3} --key-name {4} --query 'Instances[0].InstanceId' --output json".format(imageId, sgroup, count, ins_type, key_name))
    
    if err:
        elog(err, "Failed to run new instances")

    log("aws ec2 describe-instances --instance-id {0} --output json".format(instance_id))
    out, err = execute("aws ec2 describe-instances --instance-id {0} --output json".format(instance_id))

    if err:
        elog(err, "Failed to retrive instances' description")

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
        f_info = open(INFO_PATH + alias + ".json", 'w')
        f_info.write(json.dumps(baked_instance, indent=4))
        f_info.close()

        table = TableParser.loads(TABLE_PATH)
        table.add(alias, baked_instance["InstanceId"])
        table.save()

    except IOError, err:
        elog(err, "Failed to store instance infomation or update instance table")

def stop_instances(instance_names):

    global TABLE_PATH

    table = TableParser.loads(TABLE_PATH)
    instances_ids = table.findIds(instance_names)
    out,err = execute("aws ec2 stop-instances --instance-ids " + ' '.join(instances_ids))
    if err:
        elog(err, "Failed to stop instances")
    log(out)

def start_instances(instance_names):

    global TABLE_PATH

    table = TableParser.loads(TABLE_PATH)
    instances_ids = table.findIds(instance_names)
    out,err = execute("aws ec2 start-instances --instance-ids " + ' '.join(instances_ids))
    if err:
        elog(err, "Failed to start instances")
    log(out)

def terminate_instances(instance_names):
    # 1. find instnace_id and alias in table.json
    # 2. get instances infomation from ~/.amz/instances/info
    # 3. remove the corresponding infomation from ~/.ssh/config file
    # 4. remove the corresponding infomation from ~/.amz/instances/info and ~/.amz/instances/table
    # 5. terminate instances
    global TABLE_PATH
    global INFO_PATH
    global CONFIG_PATH

    table = TableParser.loads(TABLE_PATH) 
    instance_id_arr = table.findIds(instance_names)
    instance_alias_arr = table.findAlias(instance_names)

    out,err = execute('aws ec2 terminate-instances --instance-ids ' + " ".join(instance_id_arr))
    if err:
        elog(err)
    log(out)

    for alias in instance_alias_arr:
        out, err = execute("rm " + INFO_PATH + alias + ".json")
        if err:
            elog(err, "Failed to remove info file in path: " + INFO_PATH + alias + ".json")

    table.remove(instance_alias_arr)
    table.save()

    config = ConfigParser.loads(CONFIG_PATH)
    config.remove(instance_alias_arr)
    config.save()

def command(cmd):

    global TABLE_PATH
    global INFO_PATH

    if cmd[0] == "ls":
        out, err = execute("cat {0}".format(TABLE_PATH))
        if err:
            elog(err, "Failed to get instance table at path: " + TABLE_PATH)
        log(out)
        pass

    if cmd[0] == "cat":
        cmd.pop(0) # shift to left by one element
        if len(cmd) < 1:
            elog("Invalid input option", "not enough file name for cat")

        table = TableParser.loads(TABLE_PATH)
        instance_alias_arr = table.findAlias(cmd)
        for alias in instance_alias_arr:
            out, err = execute("cat " + INFO_PATH + alias + ".json")
            if err:
                elog(err, "Failed to open file: " + INFO_PATH + alias + ".json")
            log(alias + ':\n' + out + '\n')
        pass

def setKeyPath(cmd):

    global AMZ_CONFIG_PATH

    if len(cmd) < 1:
        elog("Invalid options", "insufficient values")

    with open(AMZ_CONFIG_PATH, "w") as amz_config_file:
        amz_config_file.write(cmd[0])

def test():
    setKeyPath(["/Users/yang/.ssh/aws-keys/yangKey.pem"])
    # command(["ls"])
    # command(["cat", "foo", "bar"])
    # execute("ssh foo")
    # start_instances(["foo", "bar"])
    # run_instances("ami-0531bf65", "foo", False, "ubuntu")
    # run_instances("ami-0531bf65", "bar", False, "ubuntu")
    # displayInstance(["foo", "bar"])
    # terminate_instances(["foo", "bar"])
    # global CONFIG_PATH
    # parser = ConfigParser.loads(CONFIG_PATH)
    # parser.remove(["foo", "bar"])
    # parser.save()

if __name__ == '__main__':


    HOME_DIR = os.path.expanduser("~")
    CONFIG_PATH = HOME_DIR + "/.ssh/config"
    IDENTITY_FILE = HOME_DIR + "/.ssh/aws-keys/yangKey.pem"
    TABLE_PATH = HOME_DIR + "/.amz/instances/table/table.json"
    INFO_PATH = HOME_DIR + "/.amz/instances/info/"
    AMZ_CONFIG_PATH = HOME_DIR + "/.amz/amz_config"

    # test()

    with open(AMZ_CONFIG_PATH, 'r') as key_file:
        content_string = key_file.read()
        if not content_string:
            elog("Configuration Error", "Please setup key path by using 'amz -key-path /your/path/id_ras.pem'")
        IDENTITY_FILE = content_string

    # debug mode will always be on in this program
    amz_utils.DEBUG = True 

    options = sys.argv[1:len(sys.argv)]
    op = options[0]

    if op == "-r" or op == "-run":
        run_instances(options[1:len(options)])
    elif op == "-f" or op == "-find":
        search(options[1:len(options)])
    elif op == "-s" or op == "-start":
        start_instances(options[1:len(options)])
    elif op == "-S" or op == "-stop":
        stop_instances(options[1:len(options)])
    elif op == "-t" or op == "-terminate":
        terminate_instances(options[1:len(options)])
    elif op == "-c" or op == "-command":
        command(options[1:len(options)])
    elif op == "-key-path":
        setKeyPath(options[1:len(options)])
    else:
        elog("Invalid Option", "Unkown option: " + op)

























# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 15:56:37
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-14 16:46:29

import sys
from amz_utils import *

class Host:

    def __init__(self, hostName):
        self.cache = {}
        self.hostName = hostName

    def __str__(self):
        return self.hostName + str(self.cache)

    def put(self, key, value):
        self.cache[key] = value

class loads:

    def __init__(self, path):

        try:
            f = open(path, 'r')
        except IOError, err:
            elog(err)

        self.path = path
        self.hostList = []
        lastHost = Host("dummyhost")
        for line in f.readlines():
            info = line.strip().split()
            if info[0] == "Host":
                self.hostList.append(lastHost)
                lastHost = Host(info[1])
            else:
                lastHost.put(info[0], info[1])
        self.hostList.pop(0)
        self.hostList.append(lastHost)

        f.close()

    def add(self, newHost):

        for host in self.hostList:
            if host.hostName == newHost.hostName:
                elog("multiple host name encountered: " + newHost.hostName + "\nYou need to configure " + self.path + " by yourself now")

        self.hostList.append(newHost)

    def remove(self, hostNames):

        self.hostList = filter(lambda host: host.hostName not in hostNames, self.hostList)


    def save(self):
        
        try:
            f = open(self.path, 'w')
        except IOError, err:
            elog(err)

        content = ""
        for host in self.hostList:
            content += "Host " + host.hostName + "\n"
            for key, value in host.cache.items():
                content += "    " + key + " " + value + "\n"

        f.write(content)
        f.close()

    # check if the new alias is duplicated
    def isAliasDup(self, alias):

        for host in self.hostList:
            if host.hostName == alias:
                return host
        return None

    def __str__(self):
        res = "\n"
        for host in self.hostList:
            res += host.hostName + "\n"
        return res;

def test():

    parser = loads(sys.argv[1])

    print parser

    parser.remove(["leet", "sit"])

    parser.save()

# test()





















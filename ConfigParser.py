# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 15:56:37
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-13 16:26:30

import sys

class Host:

    def __init__(self, hostname):
        self.cache = {}
        self.hostname = hostname

    def __str__(self):
        return self.hostname + str(self.cache)

    def put(self, key, value):
        self.cache[key] = value

class Config_parser:

    def __init__(self, path):
        f = open(path)

        hostlist = []
        lastHost = Host("dummyhost")
        for line in f.readlines():
            info = line.strip().split()
            if info[0] == "Host":
                hostlist.append(lastHost)
                lastHost = Host(info[1])
            else:
                lastHost.put(info[0], info[1])
        hostlist.append(lastHost)
        for host in hostlist:
            print host
        f.close()

parser = Config_parser(sys.argv[1])





















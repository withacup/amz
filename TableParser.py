# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-14 15:56:55
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-14 16:34:53

from amz_utils import *
import sys
import json

class loads:

    def __init__(self, path):
        self.path = path
        self.content = {}
        try:
            with open(self.path  , 'r') as table_file:
                json_string = table_file.read()
                if json_string:
                    self.content = json.loads(json_string)
        except IOError, err:
            elog(err)

# take instance_id or alias as input,
# returns alias
    def find(self, ids):
        return [pair[0] for pair in self.content.items() if pair[0] in ids or pair[1] in ids]

    def remove(self, aliases):
        for alias in aliases:
            if self.content.pop(alias ,0) == 0:
                elog("alias {0} not found".format(alias))

    def add(self, alias, ins_id):
        self.content[alias] = ins_id

    def save(self):
        try:
            with open(self.path, 'w') as table_file:
                table_file.write(json.dumps(self.content))
        except IOError, err:
            elog(err)

    def check(self, alias):
        return (alias in self.content)

def test():
    parser = loads(sys.argv[1])
    print parser.find(["foo"])
    parser.remove(["foo"])
    parser.add("foo", "i-03353eeeec099cd64")
    parser.check("oooo")
    parser.save()

# test()






















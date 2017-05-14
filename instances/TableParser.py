# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-14 15:56:55
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-14 16:12:49

from amz_utils import *
import sys

class loads:

    def __init__(self, path):
        self.path = path
        self.content = {}
        try:
            with open(path  , 'r') as table_file:
                json_string = table_file.read()
                if json_string:
                    self.content = json.loads(json_string)
        except IOError, err:
            elog(err)

# take instance_id or alias as input,
# returns alias
    def find(self, ids):
        return [pair[0] for pair in self.content.items() if pair[0] in ids or pair[1] in ids]




def test():
    parser = loads(sys.argv[1])
    print parser.find("foo")

print 123
test()
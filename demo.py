import json
import os.path
from amz_utils import *

# path = "/Volumes/YangFlashCard/projects/amz/instances/table/table.json"
path = "~"
print os.path.expanduser(path)
# if not os.path.exists(path):
#     out,err = execute("touch " + path)
#     if err:
#         print err
#     print out

# demo = open('./demo.json', 'r+w')
# demo_dic = {}
# json_string = demo.read()
# if json_string:
#     demo_dic = json.loads(json_string)

# demo_dic["foo"] = "aaaa"
# # print demo_dic
# print json.dumps(demo_dic, indent=4)
# demo.write("json.dumps(demo_dic, indent=4)")
# demo.close()
# myGlobal = 5

# def func1():
#     global myGlobal
#     myGlobal = 42

# def func2():
#     print myGlobal

# if __name__ == '__main__':
#     func1()
#     func2()
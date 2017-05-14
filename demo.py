import json


demo = open('./demo.json', 'r+w')
demo_dic = {}
json_string = demo.read()
if json_string:
    demo_dic = json.loads(json_string)

demo_dic["foo"] = "aaaa"
# print demo_dic
print json.dumps(demo_dic, indent=4)
demo.write("json.dumps(demo_dic, indent=4)")
demo.close()
# myGlobal = 5

# def func1():
#     global myGlobal
#     myGlobal = 42

# def func2():
#     print myGlobal

# if __name__ == '__main__':
#     func1()
#     func2()
myGlobal = 5

def func1():
    global myGlobal
    myGlobal = 42

def func2():
    print myGlobal

if __name__ == '__main__':
    func1()
    func2()
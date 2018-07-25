import threading

local = threading.local()
class Student():
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

def getInfo():
    stu = local.student
    print('this is %s, %d, %d in %s' %(stu.name, stu.age, stu.score, threading.current_thread().name))

def setInfo(name, age, score):
    local.student = Student(name, age, score)
    getInfo()

t1 = threading.Thread(target=setInfo, args=('Alice', 25, 88), name='Thread_1')
t2 = threading.Thread(target=setInfo, args=('Bob', 27, 90), name='Thread_2')
t1.start()
t2.start()
t1.join()
t2.join()
print('print complete...')
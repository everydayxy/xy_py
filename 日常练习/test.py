# class A:
#     def __init__(self,data):
#         self.data = data
#     def __setattr__(self, key, value):
#         self.__dict__['data'] = value #赋值
#         print(self.__dict__,'赋值ing')
#     def __getattr__(self, item):
#         print('赋值ing')
#
#
#
# A('a')

# def func():
#     print('this is func')
#     return 111
#
# def add(x,y):
#     return x+y
# add.func = func
# print(add.func())
# print(dir(add))
#
#
# ret = ['a','b']
# print(' '.join(ret))


# from functools import partial,wraps
# import inspect
#
# def add(x,y,*args):
#     print(args)
#     return x + y
#
#
# newadd = partial(add,1,2,3,4)
# print(inspect.signature(newadd))
# print(newadd.func,newadd.keywords,newadd.args)
#
#
# a = {'c':100}
# a.update({'a':2,'b':3})
# print(a)
#
# from functools import lru_cache

# import time
# import functools
#
#
# def logger(n):
#     def wrap(func):
#         def wrapper(*args,**kwargs):
#             ret = func(*args,**kwargs)
#             print('{}:{}'.format(n,ret))
#             return ret
#         return wrapper
#     return wrap
#
#
# @logger(2)
# @functools.lru_cache(maxsize=128 ,typed=True)
# def add(x,y,z=5):
#     time.sleep(z)
#     return x + y
#
#
# add(4,5)
# add(4.0,5)
# add(100,200)
# add(100,200)
# add(100,200)

# import functools
# @functools.lru_cache()
# def fib(n):
#     if n in (1,2):
#         return 1
#     return fib(n-2) + fib(n-1)
#
# # for i in range(10):
# #     print(fib(i+1))
# print([fib(i+1) for i in range(35)])

# import threading
# import time
#
# def worker(id):
#     count = 0
#     while True:
#         time.sleep(id)
#         if count > 10:
#             print('working {}'.format(id))
#             showthreadinfo()
#             return
#         count += 1
#
#
# def showthreadinfo():
#     print('{},{},{},{}'.format(threading.active_count(),
#     threading.main_thread(),
#     threading.current_thread(),
#     threading.enumerate()))
#
# class mythread(threading.Thread):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#     def start(self):
#         print('start~~~~')
#         super().start()
#     def run(self):
#         print('run~~~~~~')
#         super().run()
#
# if __name__ == '__main__':
#     obj = [mythread(target=worker,args=(i,)) for i in range(1,11)]
#     for i in obj:
#         i.start()
#     time.sleep(3)
#     print('@@@@@@@@@@@@@@@@@@@@@@@@')
#     if obj[0].is_alive():
#         print('alive')
#     else:
#         print('dead')
#         obj[0].start()


# class Point:
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
#     def __add__(self, other):
#         return Point(self.x + other.x,self.y + other.y)
#
# a = Point(1,5)
# b = Point(2,4)
# c = a + b
# print(c.x,c.y)


# class Base:
#     PUBLIC_CLASS_VAR = 'PUBLIC_CLASS_VAR'
#     __PRIVATE_CLASS_VAR = 'PRIVATE_CLASS_VAR'
#     def __init__(self):
#         self.public_instance_var = 'public_instance_var'
#         self.__private_instance_var = 'private_instance_var'
#     @classmethod
#     def public_class_method(cls):
#         return 'public_class_method'
#     @classmethod
#     def __private_class_method(cls):
#         return 'private_class_method'
#     @staticmethod
#     def public_static_method():
#         return 'public_static_method'
#     @staticmethod
#     def __private_static_method():
#         return 'private_static_method'
#     def public_instance_method(self):
#         return 'public_instance_method'
#     def __private_instance_method(self):
#         return 'private_instance_method'
#
# class Sub(Base):
#     def __init__(self):
#         pass
#     def print(self):
#         # print(self.PUBLIC_CLASS_VAR)
#         # print(self.__PRIVATE_CLASS_VAR)
#         # print(self.public_instance_var)
#         # print(self.__private_instance_var)
#         # print(self.public_class_method())
#         # print(self.__private_class_method())
#         # print(self.public_static_method())
#         # print(self.__private_static_method)
#         # print(self.public_instance_method())
#         print(self.__private_instance_method())
#
#
# print(Sub().__dict__ is Sub().__dict__)


# import csv
#
# with open(r"C:\Users\admin\Desktop\2019-06-04.csv", "w", newline="") as datacsv:
#     # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
#     csvwriter = csv.writer(datacsv, dialect=("excel"))
#     # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
#     csvwriter.writerow(["A", "B", "C", "D"])
#

# import threading
# import time
#
# class mythread(threading.Thread):
#     def run(self):
#         # print('run~~~~~')
#         self._target(*self._args, **self._kwargs)
#         # super().run()
#     def start(self):
#         print('start~~~~')
#         super().start()
#
#
#
# def show():
#     print('show~~~~',threading.current_thread().name,threading.main_thread().name)
#
#
# t = mythread(target=show,name='mythread1')
#
#
# t.start()
# time.sleep(4)
# t.run()
#
# print('~~~~~~~fin~~~~~~~')
#
#
# arr = map(int,[1,2,3,4,5])
#
# arr = (int(x) for x in [1,2,3,4,5])
# print(list(arr))
# print(list(arr))


# '''
# 应该是instance没有__getitem__()方法，所以不能用[]来访问
# 而instance.__dict__是字典，字典默认有__getitem__()方法，可以用[]访问
# '''
#
# class Int():
#     def __init__(self,name):
#         self.data = dict()
#         self.name = name
#     def __get__(self, instance, owner):
#         print('get {}'.format(self.name))
#         if instance is not None:
#             return self.data[instance]
#     def __set__(self, instance, value):
#         print('set {}'.format(self.name))
#         self.data[instance] = value
# class A:
#     val = Int('val')
#     def __init__(self):
#         self.val = 3
# a = A()
# a.val = 3
# print(a.val)
# print(a.__dict__)

# class Point():
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
#     def print(self,x,y):
#         print(x,y)
#
# p = Point(1,2)
# p.__dict__['z'] = 3
# print(getattr(p,'z'))
#
# getattr()


# class A:
#     def __delattr__(self, item):
#         print('deling {} oh my god'.format(item))
#     def __getitem__(self, item):
#         print('get value {}'.format(item))
#         if item in self.__dict__.keys():
#             return self.__dict__[item]
#         return 'no such key'
#     def __setitem__(self, key, value):
#         print('set value: {} to key:{}'.format(value,key))
#         self.__dict__[key] = value
#
# dic = A()
# dic['x'] = 2
# dic['y']= 4
# dic['z'] = 6
# print(dic['zzzz'],'   ',dic['x'])


# import  threading
# import time
#
# def add(x,y):
#     ret = x + y
#     print(1,ret,threading.current_thread(),threading.current_thread().name)
#     time.sleep(1)
#     print(2,ret,threading.current_thread(),threading.current_thread().name)
#     return ret
# class Mythread(threading.Thread):
#     def start(self):
#         super().start()
#     def run(self):
#         super().run()
#
# t1 = Mythread(target=add,args=(1,2),name='t1')
# t2 = Mythread(target=add,args=(1,2),name='t2')
#
# t1.run()
# t2.run()
#
# print('~~~~~~~~~~~fin~~~~~~~~~~~~')


# import multiprocessing
# import threading
# import time
#
#
# def loop(num):
#     print('looping {} {} {}'.format(num,threading.current_thread().name,multiprocessing.current_process().name))
#     time.sleep(5)
#
# def add(x,y):
#     print(x+y,multiprocessing.current_process())
#     time.sleep(5)
#     for i in range(10):
#         t = threading.Thread(target=loop,args=(i,))
#         t.start()
#
#
# if __name__ == '__main__':
#     for i in range(10):
#         p = multiprocessing.Process(target=add, args=(i + 1, i + 2))
#         p.start()


import time
import threading
import logging

def bar():
    time.sleep(10)
    print('bar')


t = threading.Thread(target=bar,daemon=True)

t.start()
# logging.error('waiting join')
# t.join()
logging.error('~~~~fin~~~~~~')
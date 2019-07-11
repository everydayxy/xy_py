# from random import randrange
#
# seq = [randrange(10**10) for i in range(100)]
# sort_seq_inc = sorted(seq)
# diff_num_ret = []
# diff_num = 0
# for idx , x in enumerate(sort_seq_inc):
#     if idx == 0:
#         previous_num = x
#         continue
#     diff_num  = x - previous_num
#     previous_num = x
#     diff_num_ret.append([idx,diff_num])
#
# print(sorted(diff_num_ret,key=lambda x: x[1]))
# differ_min_idx = sorted(diff_num_ret,key=lambda x: x[1])[0][0]
# print(sort_seq_inc[differ_min_idx - 1 ],sort_seq_inc[differ_min_idx])


# data = [3, 5, 8]
# g = (x for x in data if data.count(x) > 0)
# data = [3, 7, 9]
# print(list(g))

# a = 1
# def test():
#     global a
#     a += 1
#     return a
# print(test())
#
# import socket
#
# socket.socket.connect()


# import os
#
# for roots,dirs,files in os.walk('E:\\aaa',topdown=False):
#     print(roots,dirs,files)

# print(2.2 * 3.0 == 3.3 * 2.0)
# print(2.2 * 3.0)
# print(3.3 * 2.0)

# print(dict(map(lambda x,y=1: (x,y),zip('abcde',range(5)))))
# print(zip('abcde',range(5)))


# def old_copy_attr(dest,src):
#     dest.__doc__ = src.__doc__
#     dest.__name__ = src.__name__

# def copy_attr(src):
#     def _inner(dest):
#         dest.__doc__ = src.__doc__
#         dest.__name__ = src.__name__
#         return dest
#     return _inner
#
#
# def count_time(func):
#     @copy_attr(func)
#     # @copy_attr(func) <==> wrapper = copy_attr(func)(wraper)
#     # @copy_attr(func) ==> @_inner ==> _inner(wraper)
#     def wraper(*args,**kwargs):
#         '''
#         this is wrapper func
#         '''
#         start_time = time.time()
#         ret = func(*args,**kwargs)
#         print('func {} cost {} seconds'.format(func.__name__,time.time()-start_time))
#         return ret
#     # copy_attr(src,dest) src就是func，dest就是wraper
#     # old_copy_attr(wraper,func)
#     update_wrapper(wraper,func)
#     return wraper
#
# @count_time
# def during():
#     '''
#     this is during func
#     '''
#     print('-----------do---------')
#     time.sleep(2)
#     return 111
#
# print(during.__name__)
# print(during.__doc__)
# during()


# class run():
#     def __init__(self,bar):
#         self.bar = bar
#     def __call__(self):
#         print(self.bar)
#         return 'ok'
#
# t = run(111)
# t()
#
# def add(x:int,y:int) -> int:
#     '''
#
#     :param x:
#     :param y:
#     :return:
#     '''
#     return x +  y
#
# print(add.__annotations__['x'],type(add.__annotations__))
# print(isinstance(add.__annotations__['x'],type))


# from functools import update_wrapper,partial
# import inspect
#
# def add(x,y,z):
#     return x + y + z
#
# newadd = partial(add,1)
# print(inspect.signature(newadd))
# print(newadd(y=10,z=22))
#
#
#
# a = '/product\product/'
# print(a.strip('/\\'))


# class myDecorator(object):
#
#     def __init__(self, fn):
#         print("inside myDecorator.__init__()")
#         self.fn = fn
#
#     def __call__(self):
#         self.fn()
#         print("inside myDecorator.__call__()")
#
#
# @myDecorator
# # aFunction = myDecorator(aFunction)
# def aFunction():
#     print("inside aFunction()")
#
#
# print("Finished decorating aFunction()")
#
# aFunction()

# 输出：
# inside myDecorator.__init__()
# Finished decorating aFunction()
# inside aFunction()
# inside myDecorator.__call__()


# import os
# import datetime
# import time
#
# print(datetime.datetime.now())
# print(time.time())

# single = '五一快乐！'
# stage1 = [x for x in range(1,21,2)]
# stage2 = stage1[::-1]
# # print(stage1)
# # print(stage2)
# stage = stage1 + stage2
# max_num = max(stage)
# for line in stage:
#     print('{}{}'.format((max_num-line) * '    ',line * single))

#
# a  = '1@2@3@4'
# ret = getattr(a,)
# print(ret)

# class new():
#     @classmethod
#     def hahaha(cls):
#         print('hello world')
#
# new.hahaha()

# aa = []
# def foo():
#     aa.append(5)
#     print(aa)
# foo(),foo(),foo()

# import time
# import random
# import threading
# import logging
# import datetime
#
# def worker(event:threading.Event):
#     logging.info('worker {} is working'.format(threading.current_thread().name))
#     time.sleep(random.randint(1,5))
#     event.set()
#
# def boss(event:threading.Event):
#     start = datetime.datetime.now()
#     event.wait()
#     logging.info('worker exit {}'.format(datetime.datetime.now() - start))
#
# def start():
#     event = threading.Event()
#     b = threading.Thread(target=boss,args=(event,))
#     b.start()
#     for i in range(1,6):
#         threading.Thread(target=worker,args=(event,),name='worker {}'.format(i)).start()
#
#
# logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
# logging.info(datetime.datetime.now())
# start()

import random
import logging
import threading
import time

class Counter():
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    def inc(self):
        try:
            self._lock.acquire()
            self._value += 1
        finally:
            self._lock.release()
    def dec(self):
        try:
            self._lock.acquire()
            self._value -= 1
        finally:
            self._lock.release()

logging.basicConfig(level=logging.INFO)
counter = Counter()

def fn():
    if random.choice([-1,1]) > 0:
        logging.info('inc')
        counter.inc()
    else:
        logging.info('desc')
        counter.dec()
    time.sleep(1)

obj = [threading.Thread(target=fn) for _ in range(10)]

for i in obj:
    i.start()
for i in obj:
    i.join()

print(counter._value)
import inspect
import time
from functools import wraps


only_dict = dict()


def cache(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        '''
        本来用hash MD5实现
        现在根据老师讲的inspect模块实现的进阶版本
        :param args:
        :param kwargs:
        :return:
        '''
        # m = hashlib.md5()
        # arg = '{}'.format(sorted(list(args) + [v for k, v in kwargs.items()]))
        # print(arg)
        # m.update(arg.encode('utf8'))
        # md5 = m.hexdigest()
        # if md5 not in hash_dict.keys():
        #     ret = fn(*args,**kwargs)
        #     hash_dict[md5] = ret
        #     return ret
        # else:
        #     return hash_dict[md5]
        global only_dict
        only_tuple = tuple()
        sig = inspect.signature(fn)
        params = sig.parameters
        keys = params.keys()
        values = params.values()
        for i in zip(keys,args):
            only_tuple += i
        for k, v in sorted(kwargs.items()):
            if k not in only_tuple:
                only_tuple += (k,v)
        for k , v in sorted(params.items()):
            if v.default is not inspect._empty :
                if k not in only_tuple:
                    only_tuple += (k,v.default)
        #print(only_tuple)
        if only_tuple in only_dict.keys():
            return only_dict[only_tuple]
        ret = fn(*args, **kwargs)
        only_dict[only_tuple] = ret
        return ret
    return wrapper


from datetime import datetime
def logger(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        start = datetime.now()
        ret = fn(*args,**kwargs)
        delta = (datetime.now() - start).total_seconds()
        print(fn.__name__,delta)
        return ret
    return wrapper


@logger
@cache
def fib(n):
    if n in (1,2):
        return 1
    return fib(n-2) + fib(n-1)


@logger
@cache
def add(x,y=2,z=3):
    time.sleep(5)
    return x + y + z


# def hello(fn):
#     def wrapper():
#         print("hello, %s" % fn.__name__)
#         fn()
#         print("goodby, %s" % fn.__name__)
#     return wrapper
#
#
# @hello
# def foo():
#     print("i am foo")
#
#
# foo()
add = logger(cache(add))

print(add(1,2,3))
print(add(1))
print(add(1,y=2))
print(add(z=3,y=2,x=1))
print(add(y=2,x=1,z=3))
print(add(1,y=2,z=3))
print(add(x=1,y=2,z=3))
#print([fib(i+1) for i in range(35)])
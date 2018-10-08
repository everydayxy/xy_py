import time

def time_a(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs)
        stop_time = time.time()
        print('func costs',stop_time-start_time)
    return wrapper

# def timer(func):
#     def wrapper(name):
#         start_time = time.time()
#         func(name)
#         stop_time = time.time()
#         print('func costs',stop_time-start_time)
#     return wrapper
#
def foo(*args,**kwargs):
    time.sleep(3)
    print('%s in the foo %s' % (args,kwargs))
#
# foo = timer(foo)
# foo('xiayang')

print(foo.__name__)
foo = time_a(foo)
print(foo.__name__)
foo('jjj','aaaa',{'a':1})
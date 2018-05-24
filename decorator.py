import time

def decorator(func):
    def wrapper(*args,**kargs):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        ret = func(*args, **kargs)
        return ret
    return  wrapper


@decorator
def add(x,y):
    print(x+y)


add(2,3)



def timer(func):
    def wrapper():
        start_time = time.time()
        func()
        stop_time = time.time()
        print('cost time is %s' % (stop_time - start_time))
        print('in the timer')
    return wrapper

@timer
def main():
    time.sleep(5)
    print('in the test')


main()

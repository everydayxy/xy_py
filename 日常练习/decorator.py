import time

def timer(func):
    def wrapper():
        start_time = time.time()
        func()
        stop_time = time.time()
        print('cost time is %s' % (stop_time - start_time))
        print('in the timer')
    return wrapper


def main():
    time.sleep(5)
    print('in the test')


main = timer(main)
main()
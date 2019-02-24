import threading
import time
import multiprocessing

def thread1(n):
    print('thread %s on process %s' % (threading.get_ident(),n))

def process1(n):
    time.sleep(5)
    print('running process %s' % n)
    t = threading.Thread(target=thread1,args=(n,))
    t.start()

if __name__ == '__main__':
    for n in range(10):
        p = multiprocessing.Process(target=process1,args=(n,))
        p.start()


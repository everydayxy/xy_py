import time
import threading

def music(func):
    for i in range(10):
        print('I was listening to %s . %s' %(func,time.ctime()))
        time.sleep(2)

def movie(func):
    for i in range(2):
        print('I was watching %s ! %s' %(func,time.ctime()))
        time.sleep(5)

threads = []
t1 = threading.Thread(target=music,args=(u'最长的电影',))
t2 = threading.Thread(target=movie,args=(u'阿凡达',))
threads.append(t1)
threads.append(t2)


for t in threads:
    t.setDaemon(True)
    t.start()

t.join()

print('all over %s' % time.ctime())
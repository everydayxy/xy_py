import time
import threading


def movie(func):
    print('I am wathcing %s  at %s .' %(func,time.ctime()))
    time.sleep(5)

threads = []
t1 = threading.Thread(target=movie,args=('阿凡达',))
t2 = threading.Thread(target=movie,args=('幸福来敲门',))

threads.append(t1)
threads.append(t2)

for i in threads:
    i.start()


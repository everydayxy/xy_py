from multiprocessing import Process,Pool
import time
import os

def f(i):
    print('runnning job %s' % i)
    time.sleep(4)
def l(arg):
    print('--> exec done',os.getpid())

if __name__ == '__main__':
    pool= Pool(5)
    print(os.getpid())
    for i in range(10):
        pool.apply_async(func=f,args=(i,),callback=l) #异步执行
        #pool.apply(func=f, args=(i,))  #串行执行
    pool.close()
    pool.join()
    print('end')

from multiprocessing import Manager,Process
import os

def f(d,l):
    d[1] = 0.25
    d['2'] = 2
    d[0.24] = None
    l.append(os.getppid())
    print(d,l)

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list()
        lst_obj = []
        for i in range(10):
            p = Process(target=f,args=(d,l))
            p.start()
            lst_obj.append(p)
        for a in lst_obj:
            a.join()
        print(d)
        print(l)
        print(os.getpid(),os.getppid())

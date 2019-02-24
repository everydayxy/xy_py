from multiprocessing import Process,Queue


def run(aaa):
    aaa.put(['xiayang','222'])


if __name__ == '__main__':
    q  = Queue()
    p = Process(target=run,args=(q,))
    p.start()
    p.join()
    a = q.get()
    print(a)
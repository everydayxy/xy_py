import multiprocessing
import time
import threading

def thread_run():
    print(threading.get_ident())

def run(name):
    time.sleep(2)
    print(name)
    t = threading.Thread(target=thread_run,)
    t.start()

def main():
    obj= []
    for i in range(10):
        p = multiprocessing.Process(target=run,args=('bob {}'.format(i),))
        obj.append(p)
    for i in obj:
        i.start()
    for i in obj:
        i.join()

if __name__ == '__main__':
    main()
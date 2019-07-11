import multiprocessing
import time
import threading

g_queue = multiprocessing.Queue()

def init_queue():
    print('init g_queue start')
    while not g_queue.empty():
        g_queue.get()
    for _index in range(10):
        g_queue.put(_index)
    print('init g_queue end')
    return

def task_io(task_id):
    print('IOstart[%s] start' % task_id)
    while not g_queue.empty():
        time.sleep(5)
        try:
            data = g_queue.get(block=True,timeout=1)
            print('IOtask[%s] get data: %s' % (task_id,data))
        except Exception as excep:
            print('IOtask[%s] error: %s' % (task_id,str(excep)))
    print('IOtask[%s] end' % task_id)
    return

g_search_list = list(range(10000))

def task_cpu(task_id):
    print('CPUtask[%s] start ' % task_id)
    while not g_queue.empty():
        count = 0
        for i in range(10000):
            count += pow(3*2,3*2) if i in g_search_list else 0
        try:
            data = g_queue.get(block=True,timeout=1)
            print('CPUtask[%s] get data: %s' % (task_id,data))
        except Exception as excep:
            print('CPUtask[%s] error: %s' % (task_id,str(excep)))
    print('CPUtask[%s] end' % task_id)
    return task_id

if __name__ == '__main__':
    print('cpu count',multiprocessing.cpu_count(),'\n')
    print('=======直接执行io密集型任务=========')
    init_queue()
    time_now = time.time()
    task_io(0)
    print('直接执行io密集型任务消耗时间:',time.time()-time_now,'\n')

    print('=======多线程执行io密集型任务========')
    init_queue()
    time_now = time.time()
    thread_list = [ threading.Thread(target=task_io,args=(i,))for i in range(5)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        if t.is_alive():
            t.join()
    print('多线程执行io密集型任务消耗时间',time.time()-time_now,'\n')


    print('=====多进程执行io密集型任务============')
    init_queue()
    time_now = time.time()
    proces_list = [multiprocessing.Process(target=task_io,args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in proces_list:
        p.start()
    for p in proces_list:
        if p.is_alive():
            p.join()
    print('多进程执行io密集型任务消耗时间：',time.time()-time_now,'\n')

    print("==========直接执行CPU密集型任务==========")
    init_queue()
    time_0 = time.time()
    task_cpu(0)
    print("直接执行CPU密集型任务消耗时间：", time.time() - time_0, "\n")

    print("==========多线程执行CPU密集型任务==========")
    init_queue()
    time_0 = time.time()
    thread_list = [threading.Thread(target=task_cpu, args=(i,)) for i in range(5)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        if t.is_alive():
            t.join()
    print("多线程执行CPU密集型任务消耗时间：", time.time() - time_0, "\n")

    print("========== 多进程执行cpu密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    process_list = [multiprocessing.Process(target=task_cpu, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in process_list:
        p.start()
    for p in process_list:
        if p.is_alive():
            p.join()
    print("多进程执行cpu密集型任务消耗时间：", time.time() - time_0, "\n")

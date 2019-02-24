import time
import threading


def run(n):
    print('run task %s at \'%s\'' % (n,time.ctime()))
    time.sleep(3)
    print('task done %s ,%s' % (n,threading.current_thread()))

threads = []
for i in range(1,101):
    t = threading.Thread(target=run,args=(i,))
    threads.append(t)

start_begin = time.time()

for t in threads:
    t.setDaemon(True) #设置为守护线程
    t.start()

for t in threads:
    t.join()  #阻塞等待所有线程执行完毕

print('cost time %s ,%s ,%s' % ((time.time() - start_begin),threading.current_thread(),threading.active_count()))


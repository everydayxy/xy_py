import threading
import time

def run(n):
    semaphore.acquire()
    time.sleep(1)
    print('running the thread %s .\n' % n)
    semaphore.release()


semaphore = threading.BoundedSemaphore(5)
for i in range(23):
    t = threading.Thread(target=run,args=(i,))
    t.start()
while threading.active_count() != 1:
    pass
else:
    print('all threads done')

import time
import threading

def run(n):
    lock.acquire()
    print("task %s is running " % n)
    global num
    num-=1
    print("task %s is done " % n )
    lock.release()

lock = threading.Lock()
num = 1000

new_obj = []
for i in range(1,1001):
    t = threading.Thread(target=run,args=(i,))
    new_obj.append(t)

for t in new_obj:
    t.setDaemon(True)
    t.start()

for t in new_obj:
    t.join()


print("...all threads has finished..." , threading.current_thread(),threading.active_count())

print("num", num)
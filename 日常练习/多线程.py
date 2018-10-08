import threading
import time

class TestThread(threading.Thread):
    def __init__(self, name, event):
        super(TestThread, self).__init__()
        self.name = name
        self.event = event

    def run(self):
        print ('Thread: ', self.name, ' start at:', time.ctime(time.time()))
        self.event.wait()
        print ('Thread: ', self.name, ' finish at:', time.ctime(time.time()))

def main():
    event = threading.Event()
    threads = []
    for i in range(1, 5):
        threads.append(TestThread(str(i), event))
    print ('main thread start at: ', time.ctime(time.time()))
    event.clear()
    for thread in threads:
        thread.start()
    print ('sleep 5 seconds.......')
    time.sleep(5)
    print ('now awake other threads....')
    event.set()


main()
import queue
import threading
import time


class Prodecer(threading.Thread):
    def __init__(self, q):
        super(Prodecer, self).__init__()
        self.q = q

    def run(self):
        cont = 0
        while True:
            cont_str = '产品{}'.format(cont)
            print('生产者---' + cont_str)
            self.q.put(cont_str)
            cont += 1
            time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self, q, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name

    def run(self):
        while True:
            print('消费者{}---{}剩余产品数{}'.format(self.name, self.q.get(), self.q.qsize()))
            time.sleep(3)


def func():
    q = queue.Queue()
    Prodecer(q).start()
    Consumer(q, 1).start()
    Consumer(q, 2).start()


if __name__ == '__main__':
    func()
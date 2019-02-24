import time
re

def consumer(name):
    print('starting eating baozi --->>')
    while True:
        new_baozi = yield
        print('[%s] is eating baozi %s' % (name,new_baozi))

def producer():
    con1.__next__()
    con2.__next__()
    n = 0
    while n < 10:
        n += 1
        con1.send(n)
        con2.send(n)
        time.sleep(0.5)
        print('producer is making baozi %s' % (n))


if __name__ == '__main__':
    con1 = consumer('c1')
    con2 = consumer('c2')
    p = producer()

# 协程 ： 用单线程实现多线程的并发效果
# 协程的实现方式：遇到io操作就进行切换，并且在io操作完成以后再切换回去 利用cpu的切换速度，实现大并发的效果


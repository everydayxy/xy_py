import time

def consumer(name):
    print('%s准备吃包子了！' % name)
    while True:
        baozi = yield
        print('包子[%s]来了,被[%s]吃了' %(baozi,name))


#c = consumer('杨洋')
#
#print(c)
#print(c.__next__())
#
#
#b1 = '韭菜馅'
#c.send(b1)
#
#
#print(c.__next__())
#print(c.__next__())


def producer():
    c1 = consumer('A')
    c2 = consumer('B')
    c1.__next__()
    c2.__next__()
    print('准备开始吃包子')
    for i in range(1,11):
        time.sleep(1)
        print('#'*15)
        print('做了一个包子,分两半')
        c1.send(i)
        c2.send(i)

producer()



#协程，比线程更小的单位



# def consumer(name):
#     print('start to eat baozi')
#     while True:
#         baozi = yield
#         print('包子【{}】来了，被【{}】吃了'.format(baozi,name))
#
# c = consumer('杨某某')
# next(c)
# c.send('绿某某')
# c.send('红某某')
# next(c)
# c.send('白某某')
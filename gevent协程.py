import gevent

def foo():
    print('1')
    gevent.sleep(1)
    print('3')
def bar():
    print('2')
    gevent.sleep(2)
    print('4')

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar)
])
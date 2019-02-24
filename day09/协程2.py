from greenlet import greenlet

def test1():
    print(1)
    gr2.switch()
    print(3)
    gr2.switch()

def test2():
    print(2)
    gr1.switch()
    print(4)

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()

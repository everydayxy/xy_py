import threading
import time

event = threading.Event()

def  light():
    count = 0
    event.set()
    while True:
        if  count > 5 and count < 15:
            event.clear()
            print('\033[1;37;41mred light\033[0m')
        elif count == 16:
            event.set()
            count = 0
        else:
            print('\033[1;37;42mgreen light\033[0m')
        count += 1
        time.sleep(1)

def car(name):
    while True:
        if event.is_set():
            print('car %s is running' % name)
            time.sleep(0.4)
        else:
            print('red light is on, %s waiting' % name)
            event.wait()
            print('green light is on')


if __name__ == '__main__':
    l = threading.Thread(target=light,)
    c1 = threading.Thread(target=car,args=('car1',))
    #c2 = threading.Thread(target=car,args=('car2',))
    l.start()
    c1.start()
    #c2.start()
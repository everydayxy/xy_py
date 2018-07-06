import threading
import time

event = threading.Event()

def light():
    count = 1
    event.set()
    while True:
        if count > 3 and count < 10:
            event.clear()
            print('%s red light %s' % ('\033[0;31m','\033[0m'))
        elif count > 11:
            event.set()
            count = 1
        else:
            print('%s green light %s' % ('\033[0;32m', '\033[0m'))
        time.sleep(1)
        count += 1

def car():
    while True:
        if event.is_set():
            print('cars is runing ....')
            time.sleep(0.5)
        else:
            print('redlight , waiting...')
            event.wait()
            print('green light is on...')

if __name__ == '__main__':

    lighter = threading.Thread(target=light,)
    lighter.start()
    carer = threading.Thread(target=car,)
    carer.start()
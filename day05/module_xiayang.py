
global_name = 'yangyang'

def say_hello():
    print('hello world')


def fib(max):
    a,b,n = 0,1,1
    while n < max:
        a , b = b , a + b
        yield b
        n += 1

def logger():
    print('logger in xiayang')
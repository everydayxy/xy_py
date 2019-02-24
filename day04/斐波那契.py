

def fib(max):
    a,b,n = 0,1,1
    while n < max:
        a , b = b , a + b
        yield b
        n += 1

a = fib(10)
print(a)
while True:
     try:
         print(next(a))
     except StopIteration:
         break
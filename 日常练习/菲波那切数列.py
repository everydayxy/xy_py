
def fib(max):
    a,b,n = 0,1,1
    while n < max:
        yield b
        a , b = b , a + b
        n = n+1
    return 'hahahah__done'

lst = fib(10)
print(lst)


try:
    while True:
        print(lst.__next__())
except StopIteration as aaa:
    print(aaa.value)

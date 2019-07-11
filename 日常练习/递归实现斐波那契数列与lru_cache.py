import functools


@functools.lru_cache()
def fib(n):
    if n in (1,2):
        return 1
    return fib(n-2) + fib(n-1)


print([fib(i+1) for i in range(35)])

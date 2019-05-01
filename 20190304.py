def counteer(base):
    def inc(step=1):
        nonlocal  base
        base += step
        return base
    return inc

f1 = counteer(10)
f2 = counteer(10)
print(f1 is f2)
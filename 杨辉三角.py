def traingle():
    N = [1]
    while True:
        yield N
        N.append(0)
        N = [N[i-1] + N[i] for i in range(len(N))]

n = 0
for i in traingle():
    print(i)
    n += 1
    if n == 10:
        break
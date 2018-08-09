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

n = 4
k = 2
lst = []
for i in range(0,n+1):
    row = [1]
    lst.append(row)
    if i == 0:
        continue
    for j in range(1,i):
        row.append(lst[i-1][j-1] + lst[i-1][j])
    row.append(1)

print(lst)
print(lst[n][k])

#       1      lst[0][0] = 1
#      1 1     lst[1][0] = 1 lst[1][-1] = 1
#     1 2 1    lst[2][0] = 1 lst[2][1] = lst[1][0] + lst[1][1] = 2 lst[2][-1] = 1
#    1 3 3 1   lst[3][0] = 1 lst[3][1] = lst[2][0] + lst[2][1] = 3 lst[3][2] = lst[2][1] + lst[2][2] = 3 lst[3][-1] = 1
#   1 4 6 4 1
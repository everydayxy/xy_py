#a[n][m] = a[n-1][m-1] + a[n-1][m]

line = int(input('请输入需要求的行：'))
a = [x for x in range(line)]
for i in range(1,line+1):
    if i == 1:
        a[0] = [1]
    if i == 2:
        a[1] = [1,1]
    if i == 3:
        a[2] = [1,a[1][0] + a[1][1],1]
    # if i == 4:
    #     a[3] = [1,a[2][0] + a[2][1],a[2][1] + a[2][2],1]
    # if i == 5:
    #     a[4] = [1,a[3][0] + a[3][1],a[3][1] + a[3][2],a[3][2] + a[3][3],1]
    if i > 3:
        b = []
        for j, k in enumerate(range(i)):
            if j == 0:
                b.append(1)
            if j == i-1:
                b.append(1)
            else:
                b.append(a[i-1][j-1] + a[i-1][k-1])
        a[i-1] = b
        print(b)
for i in a:
    print(i)

# def jiecheng(x):
#     i = 1
#     j = 1
#     while i <= x:
#         j *= i
#         i += 1
#     return j
# def c(n,m):
#     n = n -1
#     m = m - 1
#     result = int(jiecheng(n)/(jiecheng(m)*jiecheng(n-m)))
#     return result
# def main():
#     while True:
#         hang = input('请输入行:')
#         lie = input('请输入列:')
#         print(c(int(hang),int(lie)))
#main()
# def aaa(n):
#     count = len(str(n))
#     w = 10 ** (count-1)
#     for _ in range(count):
#         print(n // w)
#         n %= w
#         w //= 10
#
# num = int(input('输入一个数字: '))
# aaa(num)

# #输入一个数字，打印最大值
# max1 = -100000000000000000000
# while True:
#     try:
#         num = int(input('请输入一个数字：'))
#         if num > max1:
#             max1 = num
#         end = input('输入数字结束了吗？？【y/n|Y/N】')
#         if end == 'y' or end == 'Y':
#             print('最大值为：', max1)
#             break
#     except ValueError:
#         print('检测到非法字符，请重新输入')
#         break

for i in range(1,10):
    s = ''
    for j in range(1,i+1):
        s += '{}*{}={:<4}'.format(j,i,j*i)
    print(s)
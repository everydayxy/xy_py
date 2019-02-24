# def compare(x,y,reverse=True):
#      return x > y if reverse else x < y
#
# def sort(lst,reverse=False,fn=compare):
#     new_lst = []
#     for i in lst:
#         for k,v in enumerate(new_lst):
#             if fn(i,v,reverse) :
#                 new_lst.insert(k,i)
#                 break
#         else:
#             new_lst.append(i)
#     return new_lst
#
# a = [2,34,41,7689,1,10,2]
#
# print(sort(a,reverse=True))


# def counter(base):
#     def inc(step=1):
#         nonlocal base
#         base += step
#         return base
#     return inc
#
# f1 = counter(5)
# f2 = counter(5)
# f3 = counter(5)
# print(id(f1),id(f2),id(f3))





# import subprocess
# from subprocess import Popen,PIPE
#
# proc = Popen('echo "hahah"',shell=True,stdout=PIPE)
# code = proc.wait()
# txt = proc.stdout.read()
# print(txt)
# print(code)

# import time
# def fib(n):
#     N = 2
#     a,b = 0,1
#     while N < n:
#         a,b = b,a+b
#         N += 1
#     return a
# start = time.time()
# x = (fib (i) for i in range(1,100000000))
# stop = time.time()
# print(stop-start)
# for y in range(19):
#     print(y)



#输入两个数字 ，给出最大数

# while True:
#     a = int(input('a:'))
#     b = int(input('b:'))
#
#     if a > b :
#         print(a)
#     else:
#         print(b)


# # 给定一个不超过5位的正整数，判断有几位
# itr = {
#     4: '个位',
#     3: '十位',
#     2: '百位',
#     1: '千位',
#     0: '万位'
#     }
# while True:
#     num = input('input num:')
#     try:
#         num = int(num)
#         if isinstance(str(num), str):
#             count = 0
#             for x in str(num):
#                 count += 1
#             print('count is {}'.format(count))
#             if count <= 5:
#                 for idx,s in enumerate(str(num)):
#     except ValueError:
#         print('illeagle num')

# for i in range(1,11):
#     if i%2:
#         continue
#     print(i)

#给定一个不超过5位的正整数，判断该数的位数，依次打印出十位，百位千位，万位的数字
num = int(input('》》'))
length = len(str(num))
if num < 100000 and num>=0:
    for x in range(length):
        tmp = num // 10
        print(num - ( tmp *10))
        num = tmp

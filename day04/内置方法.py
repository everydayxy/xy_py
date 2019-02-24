
print(bin(10))  # 将整形数字转换成二进制格式


#bytearray 可修改的二进制字节格式

a = bytes('abcde',encoding='utf-8')
b = bytearray('abcde',encoding='utf-8')

print(a.capitalize(),a)
print(b[0]) #打印的是a的ascii码

b[1] = 50

print(b)

code = 'for i in range(1,6):print(i)'
compile(code,'','exec')
exec(code)

code = 'print((10+2)/6)'
compile(code,'','eval')
eval(code)

code = '''
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
'''


exec(code)

#还可以将另一个文件里的代码都贴进来，然后从字符串编译成代码执行，相当于import了一个文件
#可以实现动态导入功能


print(dir(code))
#查看变量可以使用的方法


aaa = lambda n:print(n)
aaa('say hi')

res1 = filter(lambda n:n>5,range(10)) #filter 筛选所需
res2 = map(lambda n:n*n,range(10))
res3 = [i*i for i in range(10)]
print(res1)
for i in res1:
    print(i)
print('#' * 20)
print(res2)
for i in res2:
    print(i)
print(res3)

from functools import reduce
res4 = reduce(lambda x,y:x+y,range(1,101)) #reduce实现累加
res5 = reduce(lambda x,y:x*y,range(1,11)) #reduce实现阶乘
print(res4)
print(res5)



a = {9:1,8:0,-1:6,99:11,4:2}
print(a)
print(sorted(a.items()))  #按照key来排序
print(sorted(a.items(),key= lambda n:n[1])) #按照value来排序


a = ['a','b','c','d','e']
b = [1,2,3,4,5,6]
dic = {}
print(zip(a,b)) #zip 拉链函数
for i in zip(a,b):
    print(i)

def zip_func(a,b):
    if len(a) >= len(b):
        lenght = len(b)
    else:
        lenght = len(a)
    for i in range(lenght):
        dic[a[i]] = b[i]
    return dic
ret = zip_func(a,b)

print(sorted(ret.items()))

__import__('斐波那契')  #把字符串当成模块import



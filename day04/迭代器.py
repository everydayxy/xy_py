from collections import Iterable

#print(isinstance({},Iterable))

#print(isinstance(111,Iterable))

print(isinstance(iter([1,2,3,4,5]),Iterable))

print(isinstance((x for x in range(10)),Iterable))


#没有next方法的就不叫迭代器

#凡是可作用于for循环的对象都是可迭代对象

#凡是可使用next(x)或者__next__()方法的对象都是迭代器对象

a = (x for x in range(10))
print(a)


b = [x for x in range(1,11)]
print(b)

b1 = iter(b)

while True:
    try:
        print(next(b1))
    except StopIteration:
        break


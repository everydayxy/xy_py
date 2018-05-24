# class Fib(object):
#     def __init__(self):
#         self.a , self.b = 0,1
#     def __iter__(self):
#         return self
#     def __next__(self):
#         self.a ,self.b = self.b , self.a + self.b
#         if self.a > 100:
#             raise StopIteration
#         print('hha')
#         return self.a
# for i in Fib():
#     print(i)

# class Fib(object):
#     def __getitem__(self, n):
#         a , b = 0 , 1
#         for n in range(n):
#             a ,b = b , a + b
#         return a
#
# f = Fib()
# print(f[10])
# print(f[11])
# print(f[12])
# print(f[13])


class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

f = Fib()
print(f[:3])

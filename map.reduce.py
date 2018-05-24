def normalize(name):
    return '%s' % (name[0:1].upper() + name[1:].lower())

L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)



from functools import reduce
def prod(L):
    def aaa(x,y):
        return x*y
    return reduce(aaa,L)
print('3 * 5 * 7 * 9 =', prod([3,5,7,9]))



from functools import reduce
def str2float(s):
    def dict(ss):
        return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[ss]
    def fn(x,y):
        return x*10 + y
    if '.' not in s:
        a = reduce(fn, map(dict, s))
        return a
    else:
        if s.split('.')[0]:
            a = reduce(fn, map(dict, s.split('.')[0]))
        if s.split('.')[1]:
            b = reduce(fn, map(dict,s.split('.')[1]))/(10**(len(s.split('.')[1])))
        return a + b

aaa = str2float('987.233')

print(aaa)
print(type(aaa))

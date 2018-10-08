

def num_str_int(str1):
    mapping = {str(x):x for x in range(0,10)}
    f,_,l = str1.partition('.')
    ret1 = 0
    ret2 = 0
    for k,v in enumerate(f.lstrip('0')[::-1]):
        ret1 += mapping[v] * (10 ** k)
    for k,v in enumerate(l.rstrip('0')):
        k += 1
        ret2 += mapping[v] * (10 ** -k)
    return ret1 + ret2

a = num_str_int('54321.623450001')
print(type(a))
print(a)
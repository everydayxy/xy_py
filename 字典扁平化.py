user_dict1 = {'a':1,'b':{'c':{'d':100}},'fff':200}
user_dict2 = {'a':1,'b':2}
user_dict3 = {'a':1,'b':{'d':3}}


def flatmp(youdict,prefix=''):
    for k,v in youdict.items():
        if isinstance(v,dict):
            flatmp(v,prefix=prefix + k + '.')
        else:
            target[prefix+k] = v


target = dict()
flatmp(user_dict1)
print(target)

target = dict()
flatmp(user_dict2)
print(target)

target = dict()
flatmp(user_dict3)
print(target)
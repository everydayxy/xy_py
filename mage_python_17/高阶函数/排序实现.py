def sort(iterable,reverse=False,key=lambda x,y : x < y):
    ret = []
    for x in iterable:
        for k,i in enumerate(ret):
                if x < i :
                    ret.insert(k,x)
                    break
        else:
            ret.append(x)
    return ret

print(sort([1,2,10,3,2,1,-1,1020,-200],reverse=False))
print(sort([1,2,10,3,2,1,-1,1020,-200],reverse=True))
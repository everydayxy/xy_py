#第一种做法
a = [0,0,0,0,1,1,1,13,256,2,2,2,2,3,3,3]
new_lst = []
for i in a:
    if i not in new_lst:
        new_lst.append(i)
print(new_lst)

#第二种做法
a = [0,0,0,0,1,1,1,13,256,2,2,2,2,3,3,3]
s = set(a)
new_lst = []

for i in a:
    if i in s:
        new_lst.append(i)
        s.remove(i)
print(new_lst)

#第三种做法
a = [0,0,0,0,1,1,1,13,256,2,2,2,2,3,3,3]
s = set()
new_lst = []
for i in a:
    if i not in s:
        new_lst.append(i)
        s.add(i)
print(new_lst)

#第四种做法
from collections import OrderedDict
a = [0,0,0,0,1,1,1,13,256,2,2,2,2,3,3,3]
new_lst=  []
od = OrderedDict()
for x in a:
    od[x] = x
new_lst = list(od.keys())
print(new_lst)
import os


f1 = open('上海游奇联通上架服务器.txt','r',encoding='utf8')
f2 = open('联通机房宿主机.txt', 'r', encoding='utf8')

ser1 = []
for line1 in f1.readlines():
    parts1 = line1.split('|')
    ser1.append(parts1[11])

ser2 = []
for line2 in f2.readlines():
    parts2 = line2.split('|')
    ser2.append(parts2[0])

print(ser1)
print(ser2)

for i in ser1:
    if i in ser2:
        pass
    else:
        print("序列号：{} 不存在于联通机房宿主机.txt中".format(i))

#for k in ser1:
#    for kk in ser1[k]:
#        if k in ser2:
#            if kk in ser2[k]:
#                if ser1[k][kk].replace('10.0','192.168') in ser2[k][kk]:
#                    pass
#                else:
#                    print('序列号：{} ip不相等'.format(k))
#            else:
#                print("序列号：{} 机柜号不在移动机房宿主机.txt中".format(k))
#        else:
#            print("序列号：{} 不在移动机房宿主机.txt中".format(k))

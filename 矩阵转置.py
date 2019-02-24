a = [[1,2,3],[4,5,6]]

ret = []
for i,row in enumerate(a):
    for j,col in enumerate(row):
        ret[j][i] = col

print(ret)
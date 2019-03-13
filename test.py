# from random import randrange
#
# seq = [randrange(10**10) for i in range(100)]
# sort_seq_inc = sorted(seq)
# diff_num_ret = []
# diff_num = 0
# for idx , x in enumerate(sort_seq_inc):
#     if idx == 0:
#         previous_num = x
#         continue
#     diff_num  = x - previous_num
#     previous_num = x
#     diff_num_ret.append([idx,diff_num])
#
# print(sorted(diff_num_ret,key=lambda x: x[1]))
# differ_min_idx = sorted(diff_num_ret,key=lambda x: x[1])[0][0]
# print(sort_seq_inc[differ_min_idx - 1 ],sort_seq_inc[differ_min_idx])


data = [3, 5, 8]
g = (x for x in data if data.count(x) > 0)
data = [3, 7, 9]
print(list(g))
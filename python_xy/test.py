# #!/usr/bin/env python
# # coding:utf8
#
# f = open('xuqiu20181029.csv','r')
# new_dict = {}
# for line in f:
#     parts = line.split('|')
#     if int(parts[11]) == 2:
#         if parts[2] in new_dict:
#             new_dict[parts[2]] += int(parts[10])
#         else:
#             new_dict[parts[2]] = int(parts[10])
#
#
# for k,v in new_dict.items():
#     if v > 6000:
#         print(k,v)


# a = [[1, 2], [3, 4], [5, 6]]
# b = [x for l in a for x in l]
# print(b)

# a = [[1, 2], [3, 4], [5, 6]]
# flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
# print(flatten(a))
#
# def flatten(x):
#     new_lst = []
#     if type(x) is list:
#         for l in x:
#             for y in flatten(l):
#                 new_lst.append(y)
#     else:
#         new_lst = [x]
#     return new_lst
# a = [[1, 2], [3, 4], [5, 6]]
# b = flatten(a)
# print(b)


a = 2222.123
print('{:.2f}'.format(a))

a = 'Henry'
print(f"{a}")

# num = 6543210
# count = 1
# tmp = num
# while tmp > 10:
#     tmp /= 10
#     count += 1
# print(int(tmp))
# print(count)

# def solve(str):
#     count_uppper = 0
#     count_lower = 0
#     for x in str:
#         if x.islower():
#             count_lower += 1
#         if x.isupper():
#             count_uppper += 1
#     print(count_uppper,count_lower)
#     if count_lower >= count_uppper:
#         str = str.lower()
#     else:
#         str = str.upper()
#     return str
# print(solve('AAAAAAAbb'))


def solve(args:str):
    count_upper = 0
    count_lower = 0
    for x in args:
        if x.islower():
            count_lower += 1
        if x.isupper():
            count_upper += 1
    if count_lower >= count_upper:
        return args.lower()
    else:
        return args.upper()

print(solve("aaaaaaaaaaFFFF"))
import re
a = ['[123][456]234567','[123]98765[456]','[234]xxxxxxxx[657]']


def get_index(string,ret):
    if string != '' and '[' in string:
        begin = string.index('[')
        end = string.index(']')
        string1 = string[begin:end + 1]
        string2 = string[end+1:]
        ret.append(string1)
    else:
        return
    return get_index(string2,ret),ret

n_ret = []
for i in a:
    ret = []
    ret = get_index(i,ret)[1]
    n_ret.append(ret)
print(n_ret)




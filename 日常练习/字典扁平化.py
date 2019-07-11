from collections import OrderedDict

test_dict = {'a':{'b':108},'c':20,'d':{'a':{'f':3}},'e':{'g':{'z':100}}}


def dict_flat(new_dict):
    def _flat(new_dict,aim_dict=None,aim_str=''):
        if aim_dict is None:
            aim_dict = dict()
        for k,v in new_dict.items():
            if isinstance(v,dict):
                aim_str += '{}.'.format(k)
                _flat(v,aim_dict,aim_str)
            else:
                aim_str += k
                aim_dict[aim_str] = v
            aim_str = ''

    aim_dict = {}
    _flat(new_dict,aim_dict,aim_str='')
    return OrderedDict(sorted(aim_dict.items(),key=lambda x:x[1]))

print(dict_flat(test_dict))

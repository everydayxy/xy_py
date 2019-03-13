#encoding:utf-8


def read(log):
    with open(log, encoding='UTF-8') as f:
        yield from f


def make_js(log, name):
    result = {}
    for line in read(log):
        line = line.split(" ")
        if len(line) > 8:
            key = line[8]
            value = result.get(key, 0)
            result[key] = value+1
    with open('{}.js'.format(name), 'w') as f:
        f.write("res_datas={data};".format(data=result))



if __name__ == '__main__':
    make_js("access.log", "log")
import os

def walk_1(root):
    stack = [root]
    files = []
    while stack:
        cur = stack.pop()
        for x in os.scandir(cur):
            if x.is_dir():
                stack.append(x.path)
            else:
                files.append(x.path)
    return files

if __name__ == '__main__':
    for f in walk_1('D:\\桌面\\'):
        print(f)

import os

def walk_2(root):
    for x in os.scandir(root):
        if x.is_dir():
            yield from walk_2(x.path)
        else:
            yield x.path

for i in walk_2('D:\\桌面\\'):
    print(i)



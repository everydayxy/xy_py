with open('D:\\xiayang_py\\test',mode='rb') as f:
    print(f.seek(6,0))
    print(f.tell())
    print(f.read().decode())
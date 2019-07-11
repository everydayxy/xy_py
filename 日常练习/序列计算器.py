def check_key(key):
    if not isinstance(key,(int)):
        raise TypeError
    elif key < 1 :
        raise IndexError

class jianglijun:
    def __init__(self,start,stop):
        self.start = start
        self.stop = stop
        self.changed = {}

    def __getitem__(self, key):
        check_key(key)
        try:
            return self.changed[key]
        except:
            return self.start + self.stop * key
    def __setitem__(self, key, value):
        check_key(key)
        self.changed[key] = value

a = jianglijun(1,2)

print(a[3])
a[2] = 1
print(a[2])
print(a[5])
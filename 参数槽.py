
class Dict:
    def __init__(self,num):
        self.salts = []
        self.num = num
        for _ in range(num):
            self.salts.append([])
    def put(self,key,value):
        i = hash(key) % self.num
        for p,(k,v) in enumerate(self.salts[i]):
            if k == key:
                break
        else:
            self.salts[i].append((key,value))
            return
        self.salts[i][p] = (key,value)
    def get(self,key):
        i = hash(key) % self.num
        for k,v in self.salts[i]:
            if k == key:
                return v
        else:
            raise KeyError(key)

a = Dict(32)
print(a.salts)
a.put('aaa',20)
a.put('bbb','xxx')
print(a.salts)
a.put(20,20)
print(a.salts)
print(a.get('aaa'))
print(a.salts)
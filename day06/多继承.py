

class Person(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age
        print("init persion")
    def eat(self):
        print("{} is eating...".format(self.name))
    def sleep(self):
        print("{} is sleeping...".format(self.name))
    def talk(self):
        print("{} is talking...".format(self.name))

class Relation(object):
    def make_friends(self,obj):
        print("{} is making friend with {}".format(self.name,obj.name))
        self.friends.append(obj)

class Man(Relation,Person):
    def __init__(self,name,age,money):
        super(Man,self).__init__(name,age)  #新式类用法
        self.money = money
        self.friends = []
        print("init man")
    def piao(self):
        print("{} is piaoying...".format(self.name))

class Woman(Relation,Person):
    def get_birth(self):
        print("{} is born a baby...".format(self.name))

m1 = Man('mage',25,2000)
w1 = Woman('jianglijun',22)

print(m1.name,m1.age)



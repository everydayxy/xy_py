class People:

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def eat(self):
        print('%s is eating ...' % self.name)

    def sleep(self):
        print('%s is sleeping ...' % self.name)


class Man(People):

    def smoke(self):
        print('%s is smoking ... which age is %s' % (self.name,self.age))


class Woman(People):

    def get_Birth(self):
        People.eat(self)
        print('%s is get birsh , age %s' % (self.name,self.age))



m1 = Man('zhengwen',28)

w1 = Woman('jianglijun',30)

m1.smoke()
m1.sleep()

w1.get_Birth()
w1.sleep()

aaa = People('nobody',100)

aaa.sleep()



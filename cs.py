

class Role:


    def __init__(self,name,role,weapon,life_value=100,money=15000):
        #构造函数
        #在实例化时做一些类的初始化工作

        self.name = name #实例变量（静态属性），作用域就是实例本身
        self.role = role
        self.weapon = weapon
        self.__life_value = life_value
        self.money = money

#    def __del__(self):    #在实例释放或者销毁的时候自动执行
#        print('{} is dead'.format(self.name))

    def shot(self): #类的方法，功能 （动态属性）
        print('shooting...')

    #def minus_life(self,num):
     #   return self.__life_value -= num

    def got_shot(self):
        self.__life_value -= 20
        print('ah...%s am shot...  life value %s' % (self.name,self.__life_value))

    def buy_gun(self,gun_name):
        print('%s just bought %s' % (self.name,gun_name))



#print(Role)

r1 = Role('role1','police','AK47') # 实例化 初始化一个类 造一个对象 把一个类变成一个具体对象的过程 叫做实例化
r2 = Role('role2','terriost','B22') # 生成一个角色

r1.buy_gun('AK47')
r1.got_shot()
#r1.buy_gun('b51')
r2.shot()
r1.shot()
#r1.buy_gun() # 内部相当于 Role.buy_gun(r1)

#print(Role.n)
#
#print(r1.n,r1.name)
#
#print(r2.n,r2.name) #先找实例本身的，如果实例本身里没有这个变量，就是类里面找这个变量。
#
#print(r1.name)
#
#del r1.name
#r1.name = '222'
#print(r1.name)
#print(r2.name)
##
#r2.n_lst.append('from r2')

#r1.n_lst.append('from r1')




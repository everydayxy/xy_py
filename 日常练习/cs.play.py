
class Person:
    def __init__(self,name,role,weapon,life_value=100,money=10000):
        self.name = name
        self.role = role
        self.weapon = weapon
        self.__life_value = life_value
        self.money = money

    def got_shot(self):
        print("Ah.... {} got shot".format(self.name))
        self.__life_value -= 20


    def __del__(self):
        print("{} 已经没了".format(self.name))

    def show_status(self):
        print("{}'s life value is {}".format(self.name,self.__life_value))


r1 = Person('Alex','police','B51')
r2 = Person('john','terrorist','AK47')

r1.got_shot()
r1.got_shot()
r1.show_status()


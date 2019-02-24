import sys

class dog():
    def __init__(self,name):
        self.name = name
        self.__food = None
    @property
    def eat(self):
        print(self.name,'is eating',self.__food)

    @eat.setter
    def eat(self,food):
        print('set eat value',food)
        self.__food = food

d = dog('qiaozheng')
d.eat
d.eat = 'ddd'
d.eat

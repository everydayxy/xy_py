class Student(object):
    def __init__(self):
        self.__age = None

    def age_getter(self):
        return self.__age
    def age_setter(self,age):
        if isinstance(age,str) and age.isdigit():
            self.__age = int(age)
        elif isinstance(age,int):
            self.__age = age
        else:
            raise ValueError('age is illegal')
    def age_deleter(self):
        print('delete age')
    age = property(age_getter,age_setter,age_deleter)

s = Student()
s.age = '222'
print(s.age)
del s.age



class Student(object):
    def __init__(self):
        self.__age = None

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self,age):
        if isinstance(age,str) and age.isdigit():
            self.__age = int(age)
        elif isinstance(age,int):
            self.__age = age
        else:
            raise ValueError('age is illegal')
    @age.deleter
    def age(self):
        print('delete age')

s = Student()
s.age = '2333'
print(s.age)
del s.age



#两种property的实现方法


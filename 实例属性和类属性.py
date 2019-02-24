# class Student(object):
#     count = 0
#     def __init__(self,name):
#         self.name = name
#         Student.count += 1
#
# if Student.count != 0:
#     print('测试失败！1')
# else:
#     bart = Student('Bart')
#     if Student.count != 1:
#         print('测试失败！2')
#     else:
#         lisa = Student('Lisa')
#         if Student.count != 2:
#             print('测试失败！3')
#         else:
#             print('Student:',Student.count)
#             print('测试通过')

# from types import MethodType
# class Student():
#     pass
# s = Student()
# def set_age(self,age):
#     self.age = age
# s.set_age = MethodType(set_age,s)
# s.set_age(22)
# print(s.age)

# class Student(object):
#     __slots__ = ('name','age')
# s = Student()
# s.name = 'micheal'
# s.age = '56'
# class GraduateStudent(Student):
#     pass
# gs = GraduateStudent()
# gs.score = 99
# print(gs.score)

# class Student(object):
#     @property
#     def score(self):
#         return self._score
#     @score.setter
#     def score(self,value):
#         if not isinstance(value,int):
#             raise ValueError('score must be integer')
#         if value < 0 or value > 100:
#             raise ValueError('score is not illegal')
#         self._score = value
#
# s = Student()
# s.score = 98
# print(s.score)

class Screen(object):
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,value):
        # if not isinstance(value, (int,float)):
        #     raise ValueError('width must be number')
        self._width = value
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self,value):
        # if not isinstance(value, (int,float)):
        #     raise ValueError('height must be number')
        self._height = value
    @property
    def resolution(self):
        return self._width * self._height

s = Screen()
s.width = 1024
s.height = 768
print('resolution = ',s.resolution)
if s.resolution == 786432:
    print('测试通过！')
else:
    print('测试失败！')
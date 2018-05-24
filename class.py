class Student(object):

    def __init__(self,name,score):
        self.name = name
        self.score = score

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >=60:
            return 'B'
        else:
            return 'C'

    def print_socre(self):
        print('%s: %s' % (self.name, self.score))


bart = Student('jacky',70)

a = bart.get_grade()

print(a)
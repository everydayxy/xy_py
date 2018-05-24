class Base:
    def __init__(self,a,b):
        self.__a = a
        self.__b = b
    def sum(self):
        print(self.__a + self.__b)
class Sub(Base):
    def __init__(self,a,b,c):
        self.c = c
        super().__init__(a,b)

sub = Sub(1,3,3)
sub.sum()
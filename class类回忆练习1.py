

class A:
    public_var = 'public_var'
    __private_var = 'private_var'
    def __init__(self):
        self.public_instance_var = 'public_instance_var'
        self.__private_instace_var = 'private_instance_var'
    def public_method(self):
        print('public method')
    def __private_method(self):
        print('private method')
    @classmethod
    def public_class_method(cls):
        print('public_class_method')
    @classmethod
    def __private_class_method(cls):
        print('private_class_method')
    @staticmethod
    def public_static_method():
        print('public static method')
    @staticmethod
    def __private_static_method():
        print('private static method')


class B(A):
    def __init__(self):
        self.a = 'a'
        super().__init__()

class C(B):
    def __init__(self):
        self.subsub = 'subsub'
        self.public_instance_var = 'public_instance_var heiheihei'
        super(C,self).__init__()


c = C()
#print(b.public_var)
#print(b.public_method())
#print(b.__private_var())
#print(b.__private_method())
print(c.__dict__)


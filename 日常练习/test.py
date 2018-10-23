class A:
    def __init__(self,data):
        self.data = data
    def __setattr__(self, key, value):
        self.__dict__['data'] = value #赋值
        print(self.__dict__,'赋值ing')
    def __getattr__(self, item):
        print('赋值ing')



A('a')


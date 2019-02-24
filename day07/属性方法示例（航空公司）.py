class flight(object):
    '''快看 灰机'''

    def __init__(self,flight_name):
        self.flight_name = flight_name

    def flight_status(self):
        print('checking flight status',self.flight_name)
        return 0

    @property
    def flight_attribute(self):
        status = self.flight_status()
        if status == 0:
            print('{} 飞机飞走了'.format(self.flight_name))
        elif status == 1:
            print('{} 飞机到了'.format(self.flight_name))
        else:
            print('状态异常，没有对应返回结果')
        print(self.name)

    @flight_attribute.setter
    def flight_attribute(self,name):
        self.name = name
        print('正在设置值 {}'.format(self.name))

flight1 = flight('CH9800')
flight1.flight_attribute = '超时'
flight1.flight_attribute
print(flight1.__doc__)
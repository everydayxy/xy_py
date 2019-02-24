#多个超类

class Calculator:
    def calculate(self,expression):
        self.value = eval(expression)
class Talk():
    def talker(self):
        print('my value is %s' % self.value)
class TalkingCalculator(Calculator,Talk):
    pass

tc = TalkingCalculator()

tc.calculate('3*6')
tc.talker()

print(hasattr(TalkingCalculator,'talker'))

help(getattr)


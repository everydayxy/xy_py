class document:
    def __init__(self,content):
        self.content = content
class word(document):
    def __init__(self,content):
        super().__init__('word: {}'.format(content))
class excel(document):
    def __init__(self,content):
        super().__init__('excel: {}'.format(content))
def printable(cls):
    def _print(self):
        print('jianglijun: {}'.format(self.content))
    cls.print = _print
    return cls

@printable
class printableword(word):
    def __init__(self,content):
        super().__init__(content)

class printablemixin:
    def print(self):
        result = 'mixin: {}'.format(self.content)
        print(result)
        return result
class printableexcel(printablemixin,excel):
    def __init__(self,content):
        super().__init__(content)

class printablemonitor(printablemixin):
    def print(self):
        print('monitor: {}'.format(super().print()))

class printablemonitormxinword(printablemonitor,word):
    def __init__(self,content):
        super().__init__(content)

pw = printableword('abc')
pw.print()
pe = printableexcel('cba')
pe.print()
pmw = printablemonitormxinword('aaa')
pmw.print()


#给一个不能修改的类添加额外属性的两种方法


# 类 无法修改
# 扩展一些方法 写到一个mixin类里
# 写一个类，继承mixin和无法修改的类
# 新的类就具有了要扩展的方法了

# 类 无法扩展
# 扩展一些方法 写到一个mixin类里
# 写一个类，继承mixin和无法修改的类
# 新的类就具有了要扩展的方法了

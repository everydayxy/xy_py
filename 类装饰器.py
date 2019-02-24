class Document:
    def __init__(self,content):
        self.content = content
class word(Document):
    def __init__(self,content):
        super().__init__('word : {}'.format(content))
class excel(Document):
    def __init__(self,content):
        super().__init__('excel : {}'.format(content))

def printer(cls):
    def _print(self):
        print(self.content)
    cls.print = _print
    return cls
@printer
class printword(word):
    def __init__(self,content):
        super().__init__(content)

a = printword('hello world')
a.print()
class A:
    def  __init__(self):
        print('A')
class B(A):
    def __init__(self):
        print('B')
class C(A):
    pass
    #def __init__(self):
    #    print('C')
class D(B,C):
    pass

a = D()


# D属于最下面一层，B，C属于这个继承关系中的中间层，属于同一层，A属于最上面一层
# 查找时顺序，从D开始，先找B再找C，最后找A
# 广度优先概念
# 深度优先

#实际程序看到的是广度优先
#python2 支持深度优先
#python3 支持广度优先

# python2上的经典类是按照深度优先来继承的，新式类是按照广度优先来继承的
# python3上的经典类和新式类都是统一按照广度优先来继承的*96+.
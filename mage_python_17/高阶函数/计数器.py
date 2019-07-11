
def counter(base):
    def inc(step=1):
        # 表示base的值不在本地，前提是需要有嵌套，或者直接给变量赋值也行
        nonlocal base
        base += step
        return base
    return inc

a  = counter(2)
print(a(2),a(2),a(3))
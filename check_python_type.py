import inspect
import functools

def check(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kwargs):
        sig = inspect.signature(fn)
        sig_type = [v.annotation for k,v in sig.parameters.items()]
        for k,v in zip(sig_type,args):
            if k != type(v):
                return 'type error'
        else:
            ret = fn(*args, **kwargs)
            return ret
    return wrapper


@check  # add = check(add)
def add(x:int , y:int):
    return x + y


print(add(20,15))



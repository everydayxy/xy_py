import importlib
mod = __import__('lib.aa')
print(mod.aa)
obj = mod.aa.C()
print(obj.name)
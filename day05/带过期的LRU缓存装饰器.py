#  1.FIFO（First In First out）：先见先出，淘汰最先近来的页面，新进来的页面最迟被淘汰，完全符合队列。
#  2.LRU（Least recently used）:最近最少使用，淘汰最近不使用的页面
#  3.LFU（Least frequently used）: 最近使用次数最少， 淘汰使用次数最少的页面
import inspect
import functools
import datetime

def cache(maxsize=128,expire=0):
    def make_key(fn,args,kwargs):
        ret = []
        names = set()
        params = inspect.signature(fn).parameters
        keys = list(params.keys())
        for i,arg in enumerate(args):
            ret.append(keys[i],arg)
            names.add(keys[i])
        ret.extend(kwargs.items())
        names.update(kwargs.keys())
        for k ,v in params.items():
            if k not in names:
                ret.append((k,v.default))
        ret.sort(key=lambda x:x[0])
        return '&'.join('{}={}'.format(name.arg) for name,arg in ret)
    def _cache(fn):
        data = {}
        queue = []
        @functools.warps(fn)
        def wrap(*args,**kwargs):
            key = make_key(fn,args,kwargs)
            now = datetime.datetime.now().timestamp()
            if key in data.keys():
                value ,timestamp =  data(key)
                queue.remove(key)
                if expire == 0 or now - timestamp < expire:
                    queue.insert(0,key)
                    return value
                else:
                    data.pop(key)
            value = fn(*args,**kwargs)
            if len(data) >= maxsize:
                # 过期清理
                if expire != 0:
                    expires = set()
                    for k,(_,timestamp,_) in list(data.items()):   #data.items()外面套个list，这样能确保不修改可迭代对象
                        if now - timestamp >= expire:
                            expires.add(k)                           # 这里修改了data
                    for k in expires:
                        queue.remove(k)
                        data.pop(k)
            if len(data) >= maxsize:
                # 换出
                #k = sorted(data.items(),key=lambda x: x[1][2])[0][0]
                k = queue.pop()
                #取出data的items中的value，再取出value中的访问时间，再取出排序以后访问时间中最小的那个的那个，再取出最小的那个的key
                data.pop(k)
            data[key] = (value,now,now)
            queue.insert(0,key)
            return value
        return wrap
    return _cache
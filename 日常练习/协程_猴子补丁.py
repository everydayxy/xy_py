import gevent.monkey
gevent.monkey.patch_all()
import gevent,time
from urllib import request
import random

def f(url,num):
    print('GET %s'% url)
    resp = request.urlopen(url)
    data = resp.read()
    with open('index{}.html'.format(num),'w') as file:
        file.write(str(data))
    print('Recv %s bytes from %s' % (len(data),url))

async_start_time = time.time()
gevent.joinall(
    [
        gevent.spawn(f,'https://www.python.org',1),
        gevent.spawn(f,'https://www.yahoo.com',2),
        gevent.spawn(f,'https://github.com',3)
    ]
)
end_time = time.time() - async_start_time
print('cost',end_time)

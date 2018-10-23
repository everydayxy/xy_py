import webob
from webob import exc
from webob.dec import wsgify
import re
from functools import wraps
from urllib.parse import parse_qs
import os

class _Var:
    def __init__(self,data=None):
        if data is not None:
            self._data = data
        else:
            self._data  = {}
    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError('not attribute {}'.format(item))
# 通过点号调用类属性，当类属性存在时，默认调用__getattribute__方法。当类属性不存在时，会调用__getattr__方法。

    def __setattr__(self, key, value):
        if key != '_data':
            raise NotImplemented
        self.__dict__['_data'] = value


#wsgify 装饰器实现
# def wsgify(fn):
#     @wraps(fn)
#     def wrap(self,environ,start_response):
#         request = webob.Request(environ)
#         response = fn(self,request)
#         return response(environ,start_response)
#     return wrap


class Application:
    ROUTER = []

    @classmethod
    def register(cls,pattern):
        def wrap(handler):
            cls.ROUTER.append((re.compile(pattern),handler))
            #cls.ROUTER[path] = handler
            return handler
        return wrap


    @wsgify
    def __call__(self,request):
        for pattern,handler in self.ROUTER:
            m = pattern.match(request.path)
            if m:
                request.args = m.groups()
                request.kwargs = _Var(m.groupdict())
                print(request.args)
                print(m.groupdict())
                print(request.kwargs)
                return handler(request)
        raise exc.HTTPNotFound()

@Application.register('^/home$')
def home(request):
    return webob.Response(body='home page',content_type='text/plain')

@Application.register('^/$')
def index(request):
    return webob.Response(body='index page',content_type='text/plain')

@Application.register('^/hello/(?P<name>\w+)$')
def hello(request):
    #name = request.params.get('name')
    name = request.kwargs.name
    response = webob.Response()
    response.text = 'my name is {}'.format(name)
    response.content_type = 'text/plain'
    return response

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0',80,Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
import webob
from webob import exc
#from webob.dec import wsgify
from functools import wraps
from urllib.parse import parse_qs
import os

# wsgify 装饰器实现
def wsgify(fn):
    @wraps(fn)
    def wrap(self,environ,start_response):
        request = webob.Request(environ)
        response = fn(self,request)
        return response(environ,start_response)
    return wrap


class Application:
    ROUTER = {}

    @classmethod
    def register(cls,path):
        def wrap(handler):
            cls.ROUTER[path] = handler
            return handler
        return wrap


    @wsgify
    def __call__(self,request):
        try:
            return self.ROUTER[request.path](request)
        except KeyError:
            raise exc.HTTPNotFound('ooops')

@Application.register('/home')
def home(request):
    return webob.Response(body='home page',content_type='text/plain')

@Application.register('/')
def index(request):
    return webob.Response(body='index page',content_type='text/plain')

@Application.register('/hello')
def hello(request):
    name = request.params.get('name')
    age = request.params.get('age')
    response = webob.Response()
    response.text = 'my name is {},age {}'.format(name,age)
    response.content_type = 'text/plain'
    return response

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0',8001,Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
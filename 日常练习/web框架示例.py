from webob.dec import wsgify
from functools import wraps
import webob
from webob import exc

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
            raise exc.HTTPNotFound()


@Application.register('/home')
def home(request):
    lin = {}
    linshi_params = request.params
    for k , v in linshi_params.items():
        lin[k] = v
    return webob.Response(body='home page {}'.format(lin),content_type='text/plain')

@Application.register('/index')
def index(request):
    return webob.Response(body='index page',content_type='text/plain')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('0.0.0.0',8001,Application())

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
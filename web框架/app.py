import webob
# from web框架.wsgify import wsgify
from webob.dec import wsgify
from webob import exc
import re


class Application():
    ROUTER = []
    @classmethod
    def register(cls,path):
        def wrapper(handler):
            cls.ROUTER.append((re.compile(path),handler))
            return handler
        return wrapper

    @wsgify
    def __call__(self,request):
        # try:
        #     return self.ROUTER[request.path](request)
        # except KeyError:
        #     return error(request)
        for pattern ,handler in self.ROUTER:
            if pattern.match(request.path):
                return handler(request)
        else:
            raise exc.HTTPNotFound()


@Application.register('^/$')
def index(request):
    return webob.Response(body='this is root', content_type='text/plain')

@Application.register('^/hello$')
def hello(request):
    url_path_name = request.params.get('name', 'None')
    response = webob.Response()
    response.content_type = 'text/plain'
    response.status_code = 200
    response.text = 'hello {}'.format(url_path_name)
    return response

def error(request):
    return webob.Response(body='do not know what you input means',content_type='text/plain')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 80, Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
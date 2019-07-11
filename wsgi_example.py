from wsgiref.simple_server import make_server,demo_app

def demo_app(environ,start_response):
    for k,v in environ.items():
        print('{}:{}'.format(k,v))
    start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])
    return ['XXXXXXX'.encode('utf-8')]

class A:
    def __init__(self):
        pass
    def __call__(self, *args, **kwargs):
        environ = args[0]
        start_response = args[1]
        for k, v in environ.items():
            print('{}:{}'.format(k, v))
        start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])
        return ['xilanhua'.encode('utf-8')]

class B:
    def __init__(self,*args,**kwargs):
        environ = args[0]
        start_response = args[1]
        for k, v in environ.items():
            print('{}:{}'.format(k, v))
        start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])
        self.ret = ['xilanhua'.encode('utf-8')]
    def __iter__(self):
        yield from self.ret

server = make_server('0.0.0.0',9000,B)
try:
    server.serve_forever()
except KeyError:
    server.server_close()
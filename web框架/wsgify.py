import webob

def wsgify(func):
    def wrapper(self,environ,start_response):
        request = webob.Request(environ)
        response = func(self,request)
        return response(environ,start_response)
    return wrapper
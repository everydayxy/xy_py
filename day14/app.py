import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('get method')
        # u = self.get_argument('user')
        # p = self.get_argument('passwd')
        # self.write('GET {} {}'.format(u,p))
        # q =  self.get_argument('query')
        favor_list = self.get_arguments('favor')
        gender_list = self.get_arguments('gender')
        self.write('{} {}'.format(gender_list,favor_list))


    def post(self):
        print('put method')
        u = self.get_argument('user')
        p = self.get_argument('passwd')
        self.write('POST {} {}'.format(u,p))


application = tornado.web.Application([
    (r"/index", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
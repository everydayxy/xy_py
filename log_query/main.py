import os, imp

from twisted.internet import epollreactor

epollreactor.install()

from twisted.web import http
from twisted.internet import reactor

import config, util

class RequestHandler(http.Request):
    def process(self):
        path = self.path
        if path.startswith('/rest/data'):
            return self.queryData()

        elif path.startswith('/rest/statistic'):
            return self.getStatistic()

        self.finish()

    def queryData(self):
        parts = self.path.split('/')
        if len(parts) < 4:
            return self.finish()
        log_name = parts[3]
        game_id = self.getArgs('game_id')
        server_id = self.getArgs('server_id')
        if game_id == None or server_id == None:
            self.finish()
        path = config.LOG_DIR + '/' + game_id + '/' + server_id
        if not os.path.exists(path):
            self.setResponseCode(http.NOT_FOUND)
            self.finish()
        start_date = util.parseDate(self.getArgs('start_time'))
        end_date = util.parseDate(self.getArgs('end_time'))
        loginname = self.getArgs('loginname')
        search_dirs = util.listDirs(game_id, server_id, start_date, end_date)
        search_dirs.sort()
        for d in search_dirs:
            filename = path + '/' + d + '/' + log_name + '.dat'
            if not os.path.isfile(filename):
                continue
            f = file(filename, 'r')
            with(f):
                while True:
                    line = f.readline()
                    if len(line) == 0:
                        break
                    if loginname != None:
                        parts = line.split('|', 3)
                        if len(parts) < 3:
                            continue
                        if loginname != parts[1]:
                            continue
                    self.write(line)
        self.finish()

    def getStatistic(self):
        sname = self.getArgs('sname')
        if sname == None:
            return self.finish()
        try:
            if os.path.isfile(sname + '.py'):
                mod = imp.load_source(sname, sname + '.py')
            elif os.path.isfile(sname + '.pyc'):
                mod =imp.load_compiled(sname, sname + '.pyc')
            else:
                return self.finish()
        except:
            return self.finish()
        parts = self.path.split('/')
        if len(parts) < 4:
            return self.finish()
        log_name = parts[3]
        game_id = self.getArgs('game_id')
        server_id = self.getArgs('server_id')
        if game_id == None or server_id == None:
            self.finish()
        args = dict()
        for k in self.args.keys():
            args[k] = self.getArgs(k)
        return mod.run(game_id, server_id, log_name, self, args)

    def getArgs(self, name):
        args = self.args
        if not args.has_key(name):
            return None
        if len(args[name]) == 0:
            return None
        return args[name][0]


class Http(http.HTTPChannel):
    requestFactory=RequestHandler

class HttpFactory(http.HTTPFactory):
    protocol=Http

if __name__ == "__main__":
    reactor.listenTCP(config.SERVER_PORT, HttpFactory(),\
                          config.SERVER_BACKLOG, config.SERVER_ADDRESS)
    reactor.run()

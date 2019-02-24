import socketserver,os

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print('{} wrote'.format(self.client_address[0]))
                if not self.data:
                    break
                #cmd = os.popen(self.data.decode()).read()
                self.request.sendall(self.data.upper())
            except Exception as e:
                print(e)
                break



if __name__ == '__main__':
    HOST,PORT = 'localhost',9999
    server = socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    server.serve_forever()
    server.server_close()
import sys,socket,time,gevent
from gevent import monkey

monkey.patch_all()

def server(port):
    s = socket.socket()
    s.bind(('0.0.0.0',port))
    s.listen(500)
    while True:
        cli,addr = s.accept()
        gevent.spawn(handle_request,cli)  #一生成请求 就交给一个协程来处理
def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            print('Recv:',data)
            conn.send(data)
            if not data:
                conn.shutdown(socket.SHUT_WR)
    except Exception as E:
        print(E)
    finally:
        conn.close()

if __name__ == '__main__':
    server(8888)

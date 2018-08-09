import gevent.monkey
gevent.monkey.patch_all()
import gevent
import socket

def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            print('recv: ',data.decode())
            if not data:
                conn.shutdown(socket.SHUT_WR)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def server(port):
    server = socket.socket()
    server.bind(('localhost',port))
    server.listen()
    while True:
        cli,addr = server.accept()
        gevent.spawn(handle_request,cli)

server(8001)
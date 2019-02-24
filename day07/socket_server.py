import socket
import os

def hahah():
    server = socket.socket()
    server.bind(('localhost',6969))
    server.listen()
    while True:
        print('我要开始等消息了')
        conn, addr = server.accept()     # conn就是客户端连过来而在服务端为其生成的一个实例
        print('消息来了')
        # print(conn,addr)
        while True:
            data  = conn.recv(1024)
            if not data:
                print('client has lost')
                break
            info = os.popen(data.decode()).read()
            #print('recv: ',info)
            conn.send(info.encode())

    server.close()

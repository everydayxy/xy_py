import socket



def client():
    HOST = '127.0.0.1'
    PORT = 8888
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    while True:
        msg = bytes(input(">>: "),encoding='utf8')
        s.sendall(msg)
        data = s.recv(1024)
        print('Recivied',repr(data))
    s.close()

if __name__ == '__main__':
    client()
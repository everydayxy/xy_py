import socket


while True:
    client = socket.socket()
    client.connect(('127.0.0.1', 9999))
    msg = input(':>>')
    if len(msg) == 0:
        continue
    client.send(msg.encode('utf-8'))
    ack = client.recv(1024).decode()
    if ack:
        print(ack)
        buffer1 = []
        while True:
            data = client.recv(1024)
            if data:
                buffer1.append(data)
            else:
                break
        d = b''.join(buffer1)
        print('命令结果\n{}\n'.format(d.decode()))
    client.close()
import socket

client = socket.socket()
client.connect(('localhost',9999))
while True:
    msg = input(':>>')
    if len(msg) == 0:
        continue
    client.send(msg.encode('utf-8'))
    buffer = []
    while True:
        data = client.recv(1024)
        if data:
            buffer.append(data)
        else:
            break
    d = b''.join(buffer)
    print('命令结果\n{}\n'.format(d.decode()))
    client.close()
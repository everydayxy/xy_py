import socket
client = socket.socket()
client.connect(('localhost', 8001))
while True:
    msg = input(':>>')
    if not msg:continue
    client.send(msg.encode('utf-8'))
    # cmd_size = int(client.recv(1024).decode('utf-8'))
    # client.send(b'ack')
    # cmd_init = 0
    # while cmd_init <= cmd_size:
    #     data = client.recv(1024,64).decode()
    #     cmd_init += len(data)
    #     print('{}'.format(data.decode()))
client.close()
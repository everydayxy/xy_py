import socket

client = socket.socket()
client.connect(('localhost',6969))
while True:
    msg = input('recv:  ').strip()
    if len(msg) == 0:continue
    client.send(msg.encode('utf-8'))
    data = client.recv(10000)
    print('recv: ',data.decode())
client.close()
import socket
import threading
import sys

class httpserver():
    def __init__(self,ip_port):
        # 创建socket
        self.listen_socket = socket.socket()
        # 调用bind绑定到指定的IP和端口
        self.listen_socket.bind(ip_port)
        # 调用listen监听端口
        self.listen_socket.listen()

        with open('index.html', 'r') as f1:
            self.first_content = 'HTTP/1.1 200 ok\nContent-Type: text/html\nContent-Length: {}\n\n'
            self.first_content += f1.read()
        with open("image.jpg", "rb") as f2:
            data = f2.read()
            self.second_content = 'HTTP/1.1 200 ok\nContent-Type: image/jpeg\nContent-Length: {}\n\n'.format(len(data)).encode('utf8')
            self.second_content += data

    def accept_tcp(self,conn,addr):
        request = conn.recv(1024)
        # 将收到请求信息从bytes转换为string
        recv_data = request.decode("utf-8")
        print(addr,recv_data)
        method = recv_data.split(' ')[0]
        path = recv_data.split(' ')[1]
        if method == 'GET':
            if path == '/index.html' or path == '/':
                # 将发送请求信息从string转换为bytes
                conn.sendall(self.first_content.encode("utf-8"))
            elif path == '/image.jpg':
                conn.sendall(self.second_content)

    def run(self):
        while True:
            try:
                # 调用accept接受客户端的请求
                client_connection, client_address = self.listen_socket.accept()
                t = threading.Thread(target=self.accept_tcp,args=(client_connection, client_address))
                t.start()
            except KeyboardInterrupt:
                # 关闭服务器发送链接
                self.listen_socket.close()


if __name__ == '__main__':
    # 这里填入服务器端的ip端口
    ip_port = ('localhost',8888)
    f = httpserver(ip_port)
    f.run()
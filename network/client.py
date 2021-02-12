import socket

host = "127.0.0.1"
port = 5555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
print ("Connection on")


data="hello\n"
socket.send(data.encode())

while(1):
    print("hola")
    dataFromServer = socket.recv(1024);
    print('he')
    print(dataFromServer.decode())


print ("Close")
socket.close()
import socket
import threading
from copy import deepcopy

class NetworkSend(threading.Thread) :
    def __init__(self, ip, port, msg) :
        threading.Thread.__init__(self)

        self._stop_event = threading.Event()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        print ("Connection on")

    def run(self) :
        self.stopped = False
        while(1):
            #message = input().encode("utf-8")
            message = msg.encode("utf-8")
            if self.stopped :
                break
            self.s.send(message)

    def stop(self) :
        self.stopped=True


port=input("numéro de port?")
msg=input("data-->").ljust(20,' ') #padding avec le caractére espace

c = NetworkSend("127.0.0.1",int(port),msg)
c.start()


file=[]
while(1) :
    data = c.s.recv(20).decode("utf-8")
    if not data :
        print("Connection lost, press ENTER to exit")
        break
    print("recv : " + data)
    file.append(data)

def getLastMessage():
    if file!=[] :
        dt = file[0]
        file.remove(dt)
        return dt
    else :
        return []

def getAllMessages():
    fd=deepcopy(file)
    file=[]
    return fd

c.s.close()
c.stop()
c.join()
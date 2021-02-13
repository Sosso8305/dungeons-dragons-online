import socket
import threading


class NetworkSend(threading.Thread) :
    def __init__(self, ip, port) :
        threading.Thread.__init__(self)

        self._stop_event = threading.Event()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        print ("Connection on")

    def run(self) :
        self.stopped = False
        while(1):
            message = input().encode("utf-8")
            if self.stopped :
                break
            self.s.send(message)

    def stop(self) :
        self.stopped=True



c = NetworkSend("127.0.0.1",1234)
c.start()

while(1) :
    data = c.s.recv(1024).decode("utf-8")
    if not data :
        print("Connection lost, press ENTER to exit")
        break
    print("recv : " + data)

c.s.close()
c.stop()
c.join()
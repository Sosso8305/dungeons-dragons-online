import socket
import threading
from copy import deepcopy
from time import sleep

networkFPS=60
ipC="127.0.0.1"
portC=5133
sizeMESSAGE = 20 #Fuck Sofiane
class Network(threading.Thread) :
    def __init__(self, ip="valeur par défaut a enlever", port="valeur par défaut a enlever", portc=portC, ipc=ipC) :
        threading.Thread.__init__(self)
        self.file = []
        self._stop_event = threading.Event()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(1 / networkFPS)
        self.s.connect((ipc, portc))
        # self.send (connection aux autres joueurs)
        print ("Connection on\n")

    def run(self) :
        self.stopped = False
        while(not self.stopped):
            try :
                data = self.s.recv(sizeMESSAGE).decode("utf-8")
                print(f"recv : {data}")
                self.file.append(data)
            except socket.timeout :
                continue
            except :
                print("Network issue")
                self.stop()


    def getMessage(self):
        if self.file:
            return self.file.pop(0) #FIFO
        else:
            return ""

    def getAllMessages(self):
        msgL = deepcopy(self.file)
        self.file = []
        return msgL

    def send(self, msg):
        self.s.send(msg.encode("utf-8"))

    def sendList(self, msgList) :
        for msg in msgList :
            self.s.send(msg.encode("utf-8"))

    def stop(self) :
        self.s.close()
        self.stopped=True


if __name__=="__main__" :
    ipC=input("Adresse IP du C ? ")
    portC = int(input("Port du C ? "))
    Networker= Network(ipc=ipC,portc=portC)
    Networker.start()
    sleep(1)
    Networker.send("Je suis un message de test !")
    sleep(3)
    Networker.stop()
    Networker.join()
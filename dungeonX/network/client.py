import socket
import threading
from copy import deepcopy
from time import sleep

networkFPS = 60
ipC = "127.0.0.1"
portC = 5133
sizeMESSAGE = 38
encodage = "ascii"


def padding(msg, n, orientation="left"):
    """A padding function used to ensure the length of network messages (shortcut of rjust and ljust). Does the padding with '0's

    Args:
        msg (str): the message to be padded
        n (int): total length the message should be
        orientation (str, optional): The orientation of the padding. Can be "left" or "right". Defaults to "left".

    Returns:
        str: the padded message
    """
    if orientation != 'right':
        return msg.rjust(n, '0')
    else:
        return msg.ljust(n, '0')


def ipPadding(ip):
    """A function to pad ip addresses. Pads ip addresses to the XXX.XXX.XXX.XXX format regardless of their original format

    Args:
        ip (string): the ip address needed

    Returns:
        str : the ip address in the XXX.XXX.XXX.XXX format
    """
    fragment = ip.split(".")
    res = ""
    for f in fragment:
        res += padding(f, 3)
        res += "."
    return res[
        0:
        -1]  # we take the string -1 character because we add an extra dot with the loop


class Network(threading.Thread):
    def __init__(self, ipc=ipC, portc=portC, debug= False):
        """The global network class, made to ensure the connection between the C and the python. Must be started with self.start() after initialization

        Args:
            ipc (str, optional): The ip address of the LOCAL C server. Defaults to ipC (127.0.0.1).
            portc (int, optional): The port address of the LOCAL C server. Defaults to portC (5133).
            debug (bool, optional) : activate debug mode (terminal logs) or not. Defaults to False.
        """
        threading.Thread.__init__(self)
        self.debug=debug
        self.file = []
        self._stop_event = threading.Event()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(1 / networkFPS)
        self.s.connect((ipc, portc))
        print("Connection on\n")

    def run(self):
        self.stopped = False
        while (not self.stopped):
            try:
                data = self.s.recv(sizeMESSAGE)
                try :
                    data= data.decode(encodage)
                except UnicodeDecodeError :
                    print(f"Sorry, couldn't decode that :{data}")
                    continue
                if data != '':
                    self.file.append(data)
            except socket.timeout:
                continue
            except Exception as e:
                if not self.stopped:
                    print(f"Network issue : {e}")
                    self.stop()
                    raise e
            if self.debug==True and len(data) >5:
                print(f"recv : {data}")

    def connexion(self, ip, port):
        """Initiate the connexion between this game and the other games

        Args:
            ip (str): the ip address of the other player
            port (int): the external port of the C of the other player
        """
        self.send(f"conxxx{ipPadding(ip)}{padding(str(port),5)}"
                  )  # message spécial a destination du C et des autres joueurs
        


    def getMessage(self):
        """Pop the oldest message from the queue (FIFO)

        Returns:
            str: the oldest message from the queue. If the queue is empty, returns the empty string
        """
        if self.file:
            return self.file.pop(0)  #FIFO
        else:
            return ""

    def getAllMessages(self):
        """Return the queue and reset it

        Returns:
            str[]: the queue
        """
        msgL = deepcopy(self.file)
        self.file = []
        return msgL

    def send(self, msg):
        """Send a message

        Args:
            msg (str): the message to send
        """
        try :
            self.s.send(msg.encode(encodage))
        except Exception as e :
            print(f"Couldn't send message {msg} : {e}")
            return
        if self.debug==True :
            print(f"successfully sent {msg}")


    def sendList(self, msgList):
        """Sends a queue of messages (FIFO)

        Args:
            msgList (str[]): the queue of messages
        """
        for msg in msgList:
            self.s.send(msg.encode(encodage))

    def stop(self):
        """Kills properly the networking thread
        """
        self.s.close()
        self.stopped = True


if __name__ == "__main__":
    #ipC = input("Adresse IP du C ? ")
    portC = int(input("Port du C ? "))
    Networker = Network("127.0.0.1", portC)
    Networker.start()
    # i = int(input())
    # if i ==1:
    #     Networker.connexion("127.0.0.1",7777)
    #     input()
    # else:
    #     input()
    #     Networker.send("Je suis un message de test !")
    sleep(3)
    a = ["waow "," trop ", "dur ", "ca ","valait ","le coup ", "de me deranger"]
    Networker.sendList(a)
    print(Networker.getAllMessages())
    Networker.stop()
    Networker.join()
import socket


def move(tup,n): #n = 0 if current client and 1 if another client
    global positions
    if(n):
        print("tuple: ",tup)
        tup = list(tup)
        tup[0] += 1
        tup[1] -= 1
        positions[1] = tup
        #+ appel a une fonction update qui a comme but de mettre a jour les positions des persos

    return tup

#mv12,130
def create_tupel(message):
    partie1 = message[2:]
    partie1 = partie1.split(",")
    partie1[1] = partie1[1].split("\0")[0]
    return int(partie1[0]), int(partie1[1])

#mvd : move done
def make_pos(tup):
    return "mvd"+str(tup[0]) + "," + str(tup[1])



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
addr = "192.168.15.167"

try:
    s.connect((addr,port))
    received_message = s.recv(2048).decode()
    print("First message: ",received_message)
except:
    print("Connection failed\n")

print("Connected successfully!")

while True:
    positions = [(0,0),(100,100)]
    received_message = s.recv(2048).decode()
    print("Message received: ",received_message)
    if received_message[:2] == "mv":
        received_message
        tup = create_tupel(received_message)
        new_position = make_pos(move(tup,1))
        new_position = new_position.encode()
        s.send(new_position)
        print("Modified ",positions[1][0],positions[1][1])
    else:
        message = input(str(">> You: "))
        message = message.encode()
        s.send(message)

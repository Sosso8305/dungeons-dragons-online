import socket


def move(tup,n): #n = 0 if current client and 1 if another client
    global positions
    tup = list(tup)
    tup[0] += 1
    tup[1] -= 1

    if(n):
        positions[1] = tuple(tup)
        #+ appel a une fonction update qui a comme but de mettre a jour les positions des persos
    else:
        position[0] = tuple(tup)
    return tup

#mv12,130
def create_tupel(message):
    partie1 = message.split(",")
    partie1[1] = partie1[1].split("\0")[0]
    return int(partie1[0]), int(partie1[1])

#mvd : move done
def make_pos(string,tup):
    return string+str(tup[0]) + "," + str(tup[1])



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
addr = "192.168.15.167"
positions = [(0,0),(100,100)]

try:
    #Send the first position of the current player and receiving the first position of the other 
    s.connect((addr,port))
    position_ini = "10,0"
    position_ini = position_ini.encode()
    s.send(position_ini)
    print("Position sent!\n")
    received_message = s.recv(2048).decode()
    print("First message: ",received_message)
    positions[1] = create_tupel(received_message)
except:
    print("Connection failed\n")

print("Connected successfully!")

while True:
    received_message = s.recv(2048).decode()
    print("Message received: ",received_message)
    print("Position initiale de l'autre: ",positions[1])
    if received_message[:2] == "mv":
        received_message
        tup = create_tupel(received_message[2:])
        new_position = make_pos("mvd",move(tup,1))
        new_position = new_position.encode()
        s.send(new_position)
        print("Modified ",positions[1][0],positions[1][1])
    else:
        message = input(str(">> You: "))
        message = message.encode()
        s.send(message)



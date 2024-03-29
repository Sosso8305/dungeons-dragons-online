MESSAGE_SIZE_MAX = {"wlc" : [2,1,4,4], "pos": [2,1,4,4], "hps": [2,1,3,5,3], "con": [15,5],"new": [2,1,4,4], "ite": [2,1,5],"che":[2,1,4]}
MESSAGE_EXTRACTION = {"wlc" : 3, "pos" : 4, "con" : 2, "new" : 3, "hps" : 5, "ite" : 3,"che":3, "pro":2, "ans":1, "exi":1,"equ":2}

def get_character(List, ID):
    for character in List:
        if character.ID == ID:
            return character


def get(string:str, c):
    """
        This function helps extracting all the informations present before the character c
    """
    i = 0
    info = ""
    while string[i] == c or string[i] == '0':
        i += 1

    while i < len(string):
        info += string[i]
        i+=1

    return info

def check_size(string: str, n: int):
    modified_str = ""
    size = len(string)

    while n - size > 0:
        modified_str += '0'
        size += 1

    modified_str += string

    return modified_str

def extract(message):
    """ 
        This function is going to take as an argument a string and returns a list of other players' infos in string format.
        This infos will be converted into the right format in other functions.
        n : nombre d'elts a extraire
    """
    flag = message[0:3]
    n = MESSAGE_EXTRACTION[flag]
    if (flag == "wlc" or flag == "new"):
        l = [message[3:5]]+[message[5:10]]+[message[10:20]]+[message[20:22]]+[[] for k in range(3)] if flag == "wlc" else [message[3:5]] + [message[5:15]]+[[] for k in range(3)]
        info = ""
        i, m = 0, l[4:] if flag=="wlc" else l[2:]
        message = message[15:] if flag == "new" else message[22:]
        
        for liste in m:
            j = 0
            while j < n: 
                k = 0
                while k < MESSAGE_SIZE_MAX[flag][j+1] and i < len(message):
                    info += message[i]
                    i += 1
                    k += 1
                liste.append(info)
                info = ""
                j += 1
    elif (flag == "pos" or flag == "hps" or flag == "con" or flag == "ite"):
        j,i = 1 if (flag == "pos" or flag == "hps") else 0,0
        info = ""
        l = [message[3:5]] if (flag == "pos" or flag == "hps") else []
        message  = message[5:] if (flag == "pos" or flag == "hps") else message[3:]
        while j < n: 
            k = 0
            while k < MESSAGE_SIZE_MAX[flag][j] and i < len(message):
                info += message[i]
                i += 1
                k += 1
            l.append(info)
            info = ""
            j += 1
    elif (flag=="che"):
        l =  [message[3:5],message[5:9],message[9:13],message[13:]] 
    elif (flag == "pro"):
        l = [message[3:5],message[5:6],message[6:10],message[10:]] 
    elif(flag == "ans"):
        l = [message[3:5],message[5:6],message[6:10],message[10:14],message[14:]]
    elif(flag == "exi"):
        l = [message[3:]]
    elif(flag == "equ"):
        l = [message[3:5],message[5:6],message[6:]]
    return l

def read_position(position_str0, position_str1):
    """
        since we receive the position as a string this function's goal is simply to convert the first string to u tuple and replace it in the list
    """
    return int(position_str0),int(position_str1)  

def read_mod(type_str):
    if type_str == 'R':
        return 'lizard_m'
    elif type_str == 'F':
        return 'knight_m'
    elif type_str == 'M':
        return 'wizzard_m'

def read_attributes(att_str):
    """
        the same functionality of the previous function but for attributes
    """
    att_str = get(att_str,'(')
    attributes_list = att_str.split(",")
    attributes_list[len(attributes_list)-1] = attributes_list[len(attributes_list)-1][:len(attributes_list[len(attributes_list)-1])-1]
    return int(attributes_list[0]),int(attributes_list[1]),int(attributes_list[2]),int(attributes_list[3]),int(attributes_list[4]) \
        ,int(attributes_list[5]) ,int(attributes_list[6]) ,int(attributes_list[7]) 

def read_IP(IP_str):
    liste_nb = IP_str.split(".")
    liste_nb[0] = str(int(liste_nb[0]))
    return ".".join(liste_nb)

def read_name(namePadd):
    i = 0
    while i < len(namePadd) and namePadd[i] == '0': i += 1
    return namePadd[i:]

class Message:
    def __init__(self, PlayerList= [], EnemyList = [], flag="", IP=0,port=0,ID = 0):
        
        self.flag = flag
        self.players = PlayerList
        self.enemies = EnemyList
        self.playerID = ID

        self.Player1Type1 = PlayerList[0]
        self.Player1Type2 = PlayerList[1] 
        self.Player1Type3 = PlayerList[2] 

        self.id1 = PlayerList[0].ID if PlayerList[0] != None else 0
        self.id2 = PlayerList[1].ID if PlayerList[1] != None else 0
        self.id3 = PlayerList[2].ID if PlayerList[2] != None else 0

        self.type1 = PlayerList[0].initialType if PlayerList[0] != None else ""
        self.type2 = PlayerList[1].initialType if PlayerList[1] != None else ""
        self.type3 = PlayerList[2].initialType if PlayerList[2] != None else ""

        self.pos1 = PlayerList[0].pos if PlayerList[0] != None else (None,None)       
        self.pos2 = PlayerList[1].pos if PlayerList[1] != None else (None,None) 
        self.pos3 = PlayerList[2].pos if PlayerList[2] != None else (None,None) 
        self.positions = [self.pos1,self.pos2,self.pos3]

        self.IP = IP
        self.port = port

        self.list1 = [self.type1,self.pos1[0],self.pos1[1]]
        self.list2 = [self.type2,self.pos2[0],self.pos2[1]]
        self.list3 = [self.type3,self.pos3[0],self.pos3[1]]
        

    def create_message(self, ID = 0, IDenemy = 0, IDItem = 0, seed="00123", positions=[], pos=(0,0), ChestPos=(0,0), prop = 0, chestContent="", index=0):

        """
            this function convert the list containing the player's characters' infos and convert them to a string 
            that will be sent to the other connected players.
        """
        message_str = self.flag + check_size(str(self.playerID),2) if(self.flag != "con") else self.flag
        if (self.flag == "wlc"): 
            message_str += check_size(str(seed),5) + check_size(self.Player1Type1.getName(),10) + check_size(str(ID),2)
            liste = [self.list1,self.list2,self.list3]
            for i in range(3):
                for j in range(len(liste[i])):
                    if (j==0):
                        part = liste[i][j]
                    else:
                        part = str(liste[i][j])
                    message_str += check_size(part,MESSAGE_SIZE_MAX[self.flag][j+1])

        elif (self.flag == "new"): 
            message_str += check_size(self.Player1Type1.getName(),10)
            liste = [self.list1,self.list2,self.list3]
            for i in range(3):
                for j in range(len(liste[i])):
                    if (j==0):
                        part = liste[i][j]
                    else:
                        part = str(liste[i][j])
                    message_str += check_size(part,MESSAGE_SIZE_MAX[self.flag][j+1])
        else: 
            ID_str = str(ID)

            if self.flag == "pos":
                message_str += check_size(ID_str,MESSAGE_SIZE_MAX[self.flag][1]) + check_size(str(pos[0]),MESSAGE_SIZE_MAX[self.flag][2]) + check_size(str(pos[1]),MESSAGE_SIZE_MAX[self.flag][3])

            elif (self.flag == "hps"):
                IDE_str = str(IDenemy)
                player = get_character(self.players, ID)
                enemy = get_character(self.enemies, IDenemy)
                HP_str = str(player.getHP())
                HP_str_e = str(enemy.getHP())
                message_str += check_size(ID_str,MESSAGE_SIZE_MAX[self.flag][1]) + check_size(HP_str, MESSAGE_SIZE_MAX[self.flag][2]) + check_size(IDE_str, MESSAGE_SIZE_MAX[self.flag][3]) + check_size(HP_str_e, MESSAGE_SIZE_MAX[self.flag][4])
            
            elif (self.flag == "con"):
                message_str += check_size(str(self.IP),MESSAGE_SIZE_MAX[self.flag][0]) + check_size(str(self.port),MESSAGE_SIZE_MAX[self.flag][1])
            
            elif (self.flag == "ite"):
                message_str += check_size(ID_str,MESSAGE_SIZE_MAX[self.flag][1]) + check_size(str(IDItem),MESSAGE_SIZE_MAX[self.flag][2])
            
            elif (self.flag == "che"):
                message_str += check_size(str(ChestPos[0]),4) +  check_size(str(ChestPos[1]),4) + check_size(chestContent,4)   

            elif (self.flag == "pro"):
                message_str += str(ID) + check_size(str(pos[0]),4) + check_size(str(pos[1]),4)
            
            elif (self.flag == "ans"):
                message_str += str(ID) + check_size(str(pos[0]),4) + check_size(str(pos[1]),4)+str(prop)

            elif (self.flag == "equ"):
                message_str += str(ID) + check_size(str(index),1)            
        return message_str
        

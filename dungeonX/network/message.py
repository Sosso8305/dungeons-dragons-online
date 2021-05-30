from dungeonX.characters.players.player import Player, PlayerEnum
from dungeonX.characters.enemies.enemy import Enemy

MESSAGE_SIZE_MAX = {"wlc" : [2,1,1,4,4], "pos": [2,1,4,4], "hps": [2,1,3,5,3], "con": [15,5],"new": [2,1,4,4], "ite": [2,1,5]}
MESSAGE_EXTRACTION = {"wlc" : 4, "pos" : 4, "con" : 2, "new" : 3, "hps" : 5, "ite" : 3}

def get_character(List, ID):
    for character in List:
        if character.ID == ID:
            return character



def get_initial(ptype):
    if ptype == PlayerEnum.Rogue:
        return 'R'
    elif ptype == PlayerEnum.Fighter:
        return 'F'
    elif ptype == PlayerEnum.Mage:
        return 'M'

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
        l = [message[3:5]]+[message[5:10]]+[message[10:20]]+[[] for k in range(3)] if flag == "wlc" else [message[3:5]] + [message[5:15]]+[[] for k in range(3)]
        info = ""
        i, m = 0, l[3:] if flag=="wlc" else l[2:]
        message = message[15:] if flag == "new" else message[20:]
        
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

    return l

def read_position(position_str0, position_str1):
    """
        since we receive the position as a string this function's goal is simply to convert the first string to u tuple and replace it in the list
    """
    return int(position_str0),int(position_str1)  

def read_type(type_str):
    """
        this function convert the str to the right type
    """

    if type_str == 'R':
        return PlayerEnum.Rogue
    elif type_str == 'F':
        return PlayerEnum.Fighter
    elif type_str == 'M':
        return PlayerEnum.Mage

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
    while namePadd[i] == '0': i += 1
    return namePadd[i:]

class Message:
    def __init__(self, PlayerList = [Player], EnemyList = [Enemy], flag="", IP=0,port=0):
        
        self.flag = flag
        self.players = PlayerList
        self.enemies = EnemyList
        self.playerID = 1 #we have to change this when we create the Player Class

        self.Player1Type1 = PlayerList[0]
        self.Player1Type2 = PlayerList[1] 
        self.Player1Type3 = PlayerList[2] 

        self.id1 = PlayerList[0].ID if PlayerList[0] != None else 0
        self.id2 = PlayerList[1].ID if PlayerList[1] != None else 0
        self.id3 = PlayerList[2].ID if PlayerList[2] != None else 0

        self.type1 = PlayerList[0].PlayerType if PlayerList[0] != None else ""
        self.type2 = PlayerList[1].PlayerType if PlayerList[1] != None else ""
        self.type3 = PlayerList[2].PlayerType if PlayerList[2] != None else ""

        self.pos1 = PlayerList[0].pos if PlayerList[0] != None else (None,None)       
        self.pos2 = PlayerList[1].pos if PlayerList[1] != None else (None,None) 
        self.pos3 = PlayerList[2].pos if PlayerList[2] != None else (None,None) 
        self.positions = [self.pos1,self.pos2,self.pos3]

        self.IP = IP
        self.port = port

        self.list1 = [self.id1,self.type1,self.pos1[0],self.pos1[1]]
        self.list2 = [self.id2,self.type2,self.pos2[0],self.pos2[1]]
        self.list3 = [self.id3,self.type3,self.pos3[0],self.pos3[1]]
        
        #self.name = PlayerList[0].name if PlayerList[0] != None else ""
        #TODO : add bag to the last list and add equiment message 

    def create_message(self, ID = 0, IDenemy = 0, IDItem = 0, seed="00123"):
        """
            this function convert the list containing the player's characters' infos and convert them to a string 
            that will be sent to the other connected players.
        """
        message_str = self.flag + check_size(str(self.playerID),2) if(self.flag != "con") else self.flag
        if (self.flag == "wlc"): 
            message_str += check_size(str(seed),5) + check_size(self.Player1Type1.getName(),10) #I am supposing that the seed = 123
            liste = [self.list1,self.list2,self.list3]
            for i in range(3):
                for j in range(len(liste[i])):
                    if (j==1):
                        part = get_initial(liste[i][j])
                    else:
                        part = str(liste[i][j])
                    message_str += check_size(part,MESSAGE_SIZE_MAX[self.flag][j+1])
        elif (self.flag == "new"): 
            message_str += check_size(self.Player1Type1.getName(),10)
            liste = [self.list1[1:],self.list2[1:],self.list3[1:]]
            for i in range(3):
                for j in range(len(liste[i])):
                    if (j==0):
                        part = get_initial(liste[i][j])
                    else:
                        part = str(liste[i][j])
                    message_str += check_size(part,MESSAGE_SIZE_MAX[self.flag][j+1])
        else: 
            ID_str = str(ID)

            if self.flag == "pos":
                player = get_character(self.players, ID)
                message_str += check_size(ID_str,MESSAGE_SIZE_MAX[self.flag][1]) + check_size(str(player.pos[0]),MESSAGE_SIZE_MAX[self.flag][2]) + check_size(str(player.pos[1]),MESSAGE_SIZE_MAX[self.flag][3])

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
            
        return message_str
        

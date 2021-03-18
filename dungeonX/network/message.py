from dungeonX.characters.players.player import Player, PlayerEnum
from dungeonX.characters.enemies.enemy import Enemy
#from dungeonX.game import Game

#To modify, for the moment it indicates the maximum size of: ID, PlayerType, xPosition, yPosition,Attributes, HP (defined as strings, the sizes' list depends on the flag)
MESSAGE_SIZE_MAX = {0 : [5,19,4,4,33], 1: [5,4,4], 2: [5,3,5,3]}

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

def extract(message, flag: int, n:int):
    """ 
        This function is going to take as an argument a string and returns a list of other players' infos in string format.
        This infos will be converted into the right format in other functions.
    """

    if (not flag):
        l = [[] for k in range(3)]
        info = ""
        i = 0
        
        for liste in l:
            j = 0
            while j < n: #This should change if we send more infos i am supposing that  we're sending only for the moment:ID, type, position and attributes 
                k = 0
                while k < MESSAGE_SIZE_MAX[flag][j] and i < len(message):
                    info += message[i]
                    i += 1
                    k += 1
                liste.append(info)
                info = ""
                j += 1
    elif (flag):
        j,i = 0,0
        info = ""
        l = []
        message  = message[1:]
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

def read_id(id_str):
    return int(id_str)

def read_position(position_str0, position_str1):
    """
        since we receive the position as a string this function's goal is simply to convert the first string to u tuple and replace it in the list
    """
    return int(position_str0),int(position_str1)  

def read_type(type_str):
    """
        this function convert the str to the right type
    """

    if get(type_str,'0') == 'PlayerEnum.Rogue':
        return PlayerEnum.Rogue
    elif get(type_str,'0') == 'PlayerEnum.Fighter':
        return PlayerEnum.Fighter
    elif get(type_str,'0') == 'PlayerEnum.Mage':
        return PlayerEnum.Mage

def read_mod(type_str):
    if get(type_str,'0') == 'PlayerEnum.Rogue':
        return 'lizard_m'
    elif get(type_str,'0') == 'PlayerEnum.Fighter':
        return 'knight_m'
    elif get(type_str,'0') == 'PlayerEnum.Mage':
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

def read_HP(hp_str):
    return int(hp_str) 


class Message:
    def __init__(self, PlayerList = [Player], EnemyList = [Enemy], flag = 0):
        
        self.flag = flag
        self.players = PlayerList
        self.enemies = EnemyList

        self.Player1Type1 = PlayerList[0]
        self.Player1Type2 = PlayerList[1] 
        self.Player1Type3 = PlayerList[2] 

        self.id1 = PlayerList[0].ID
        self.id2 = PlayerList[1].ID
        self.id3 = PlayerList[2].ID

        self.type1 = PlayerList[0].PlayerType
        self.type2 = PlayerList[1].PlayerType
        self.type3 = PlayerList[2].PlayerType

        self.pos1 = PlayerList[0].pos              
        self.pos2 = PlayerList[1].pos
        self.pos3 = PlayerList[2].pos
        self.positions = [PlayerList[0].pos ,PlayerList[1].pos ,PlayerList[2].pos]

        self.attributes1 = PlayerList[0].stats
        self.attributes2 = PlayerList[1].stats
        self.attributes3 = PlayerList[2].stats 

        # self.equipment1 = self.extract_items_ids(PlayerList[0].equipment)
        # self.equipment2 = self.extract_items_ids(PlayerList[1].equipment)
        # self.equipment3 = self.extract_items_ids(PlayerList[2].equipment)

        # self.items = self.extract_items_ids(self.Player1Type1.messageBag.content)


        # self.enemiesHP = None #a changer une fois defini
        # un dictionnaire vide 
        #on va ajouter cet attribut a la classe player et ce dictionnaire serait rempli a chaque attaque

        self.list1 = [self.id1,self.type1,self.pos1[0],self.pos1[1],self.attributes1]
        self.list2 = [self.id2,self.type2,self.pos2[0],self.pos2[1],self.attributes2]
        self.list3 = [self.id3,self.type3,self.pos3[0],self.pos3[1],self.attributes3]
        #TODO : add bag to the last list and add equiment message 

    def create_message(self, ID = 0, IDenemy = 0):
        """
            this function convert the list containing the player's characters' infos and convert them to a string 
            that will be sent to the other connected players.
        """
        message_str = ""
        if (not self.flag): 
            liste = [self.list1,self.list2,self.list3]
            for i in range(3):
                for j in range(len(liste[i])):
                    part = str(liste[i][j])
                    message_str += check_size(part,MESSAGE_SIZE_MAX[0][j])

        elif (self.flag): 
            ID_str = str(ID)

            if self.flag == 1:
                player = get_character(self.players, ID)
                message_str += str(self.flag) + check_size(ID_str,MESSAGE_SIZE_MAX[1][0]) + check_size(str(player.pos[0]),MESSAGE_SIZE_MAX[1][1]) + check_size(str(player.pos[1]),MESSAGE_SIZE_MAX[1][2])

            elif self.flag == 2:
                IDE_str = str(IDenemy)
                player = get_character(self.players, ID)
                enemy = get_character(self.enemies, IDenemy)
                HP_str = str(player.getHP())
                HP_str_e = str(enemy.getHP())
                message_str += str(self.flag) + check_size(ID_str,MESSAGE_SIZE_MAX[2][0]) + check_size(HP_str, MESSAGE_SIZE_MAX[2][1]) + \
                    check_size(IDE_str, MESSAGE_SIZE_MAX[2][0]) + check_size(HP_str_e, MESSAGE_SIZE_MAX[2][1])
            
        return message_str
        


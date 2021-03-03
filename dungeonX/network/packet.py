from dungeonX.characters.players.player import Player, PlayerEnum
#from dungeonX.game import Game

sizeMax = [7,19,11,33] #To modify, for the moment it indicates the maximum size of: ID, PlayerType, Position,Attributes (defined as strings)

def get(string:str, c):
    """
        This function helps extracting all the informations present before the character c
    """
    i = 0
    info = ""
    while string[i] != c:
        info += string[i]
        i += 1

    return info

def check_size(string: str, n: int):
    while len(string) < n:
        string += '0'

    return string 

def extract(message):
    """ 
        This function is going to take as an argument a string and returns a list of other players' infos in string format.
        This infos will be converted into the right format in other functions.
    """
    l = [[] for k in range(3)]
    info = ""
    i = 0
    
    for liste in l:
        j = 0
        while j < 4: #This should change if we send more infos i am supposing that  we're sending only for the moment:ID, type, position and attributes 
            k = 0
            while k < sizeMax[j] and i < len(message):
                info += message[i]
                i += 1
                k += 1
            liste.append(info)
            info = ""
            j += 1
    return l

def read_id(id_str):

    i = 0
    info = ""
    print(id_str)
    while (i+2 < len(id_str) and id_str[i:i+2] != "ID"):
        info += id_str[i]
        i += 1
    return int(info)

def read_position(position_str):
    """
        since we receive the position as a string this function's goal is simply to convert the first string to u tuple and replace it in the list
    """
    position_str = get(position_str,')')
    position_list = position_str.split(",")
    return int(position_list[0][1:]),int(position_list[1])  

def read_type(type_str):
    """
        this function convert the str to the right type
    """

    if get(type_str,'0') == 'PlayerEnum.Rogue':
        return PlayerEnum.Rogue
    elif get(type_str,'0') == 'PlayerEnum.Fighter':
        return PlayerEnum.Fighter
    return PlayerEnum.Rogue

def read_mod(type_str):
    if type_str == 'PlayerEnum.Rogue':
        return 'lizard_m'
    elif type_str == 'PlayerEnum.Fighter':
        return 'knight_m'
    return 'wizzard_m'

def read_attributes(att_str):
    """
        the same functionality of the previous function but for attributes
    """
    att_str = get(att_str,')')
    attributes_list = att_str.split(",")
    attributes_list[0] = attributes_list[0][1:]
    return int(attributes_list[0]),int(attributes_list[1]),int(attributes_list[2]),int(attributes_list[3]),int(attributes_list[4]) \
        ,int(attributes_list[5]) ,int(attributes_list[6]) ,int(attributes_list[7])  

def read_enemies_dict(dict_str):
    """
        this function is used to extract the dictionnary of monsters (affected by the player) from the received string packet
    """
    dict_list = dict_str.split(",")
    d = {}
    dict_list[0] = dict_list[0][1:]
    dict_list[len(dict_list)-1] = dict_list[len(dict_list)-1][:len(dict_list[len(dict_list)-1])-1]

    for i in range(len(dict_list)):
        l = dict_list[i].split(":")
        d[int(l[0])] = int(l[1])
    return d

def read_list(list_str):
    """
        this function is used to extract the list of properties' ids (the player's properties)
    """
    #it should read items in bag and see those equiped and not in the bag 
    items_list_str = list_str.split(",")
    items_list_str[0] = items_list_str[0][1:]
    items_list_str[len(items_list_str) - 1] = items_list_str[len(items_list_str) - 1][:len(items_list_str[len(items_list_str) - 1]) - 1]
    items_ids = []
    for i in range(len(items_list_str)):
        items_ids.append(int(items_list_str[i]))
    return items_ids

class Packet:
    def __init__(self, PlayerList = [Player]):
    
        self.Player1Type1 = PlayerList[0]
        self.Player1Type2 = PlayerList[1] #a changer voir zineb #done Chris
        self.Player1Type3 = PlayerList[2] #a changer voir zineb

        self.id1 = PlayerList[0].ID
        self.id2 = PlayerList[1].ID
        self.id3 = PlayerList[2].ID

        self.type1 = PlayerList[0].PlayerType
        self.type2 = PlayerList[1].PlayerType
        self.type3 = PlayerList[2].PlayerType

        self.pos1 = PlayerList[0].pos              #on peut supprimer ces 3 et les mettre dans une seule liste c un choix a faire
        self.pos2 = PlayerList[1].pos
        self.pos3 = PlayerList[2].pos
        self.positions = [PlayerList[0].pos ,PlayerList[1].pos ,PlayerList[2].pos]

        self.attributes1 = PlayerList[0].stats
        self.attributes2 = PlayerList[1].stats
        self.attributes3 = PlayerList[2].stats 

        self.equipment1 = self.extract_items_ids(PlayerList[0].equipment)
        self.equipment2 = self.extract_items_ids(PlayerList[1].equipment)
        self.equipment3 = self.extract_items_ids(PlayerList[2].equipment)

        self.items = self.extract_items_ids(self.Player1Type1.packetBag.content)


        self.enemiesHP = None #a changer une fois defini
        # un dictionnaire vide 
        #on va ajouter cet attribut a la classe player et ce dictionnaire serait rempli a chaque attaque

        self.list1 = [self.id1,self.type1,self.pos1,self.attributes1]
        self.list2 = [self.id2,self.type2,self.pos2,self.attributes2]
        self.list3 = [self.id3,self.type3,self.pos3,self.attributes3]
        #TODO : add bag to the last list and add equiment packet 

    def extract_items_ids(self,content):
        idItemList = []

        for item in content:
            if item != None:
                idItemList.append(item.id)
        
        return idItemList

    def create_packet(self):
        """
            this function convert the list containing the player's characters' infos and convert them to a string 
            that will be sent to the other connected players.
        """

        liste = [self.list1,self.list2,self.list3]
        packet_str = ""
        for i in range(3):
            for j in range(len(liste[i])):
                part = str(liste[i][j])
                if (not j):
                    part += "ID"
                packet_str += check_size(part,sizeMax[j])

        return packet_str



s="12ID000PlayerEnum.Rogue000(1,2)000000(100,2,4,5,6,7,66,56)000000000000PlayerEnum.Mage0000(22,3)00000\
(100,2,4,5,6,7,66,56)000000000000PlayerEnum.Rogue000(122,22)000(100,2,4,5,6,7,66,56)000000000000"

#print("".join(extract(s,"//perso//")))
#( HP, armor, strength, dex, con, intell, wis, cha )
# l = read_packet(s)
print(extract(s))
# print(l)
# l[0][1] = read_position(l[0][1])
# l[0][2] = read_attributes(l[0][2])
# print(l[0][0],l[0][1],l[0][2]) 

from dungeonX.characters.players.player import Player, PlayerEnum
from dungeonX.game import Game

def extract(packet_str,code):
    """ 
        if we have as an argument: codehicode this function returns hi 
        This function's main purpose is to help decode the str sent by other players
    """
    i, k = 0 , len(code)
    info = "" 
    l = []
    while i < len(packet_str):
        if packet_str[i:i+k] == code:
            l.append(info)
            info = ""
            if i+k < len(packet_str):
                i += k
            else: 
                break
        info += packet_str[i]
        i += 1
    return l

def read_packet(received_packet):
        """
            this function will return a list containing other players informations in the format: [list1,list2,list3]
            where list1 contains the infos of the other player's first character: [instance,position,attributes,properties,capacity]
            and the same is for list2 and the list3.
        """
    
        liste=[]
        message = extract(received_packet,"//perso//")
        for j in range(len(message)):
            liste.append(extract(message[j],"//$$//"))
        
        return liste

def read_position(position_str):
    """
        since we receive the position as a string this function's goal is simply to convert the first string to u tuple and replace it in the list
    """
    position_list = position_str.split(",")
    return int(position_list[0][1:]),int(position_list[1][:len(position_list[1])-1])  

def read_attributes(att_str):
    """
        the same functionality of the previous function but for attributes
    """
    attributes_list = att_str.split(",")
    return int(attributes_list[0][1:]),int(attributes_list[1]),int(attributes_list[2]),int(attributes_list[3]),int(attributes_list[4]) \
        ,int(attributes_list[5]) ,int(attributes_list[6]) ,int(attributes_list[7][:len(attributes_list[7])-1])  

def read_monsters_dict(dict_str):
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

def read_properties_list(list_str):
    """
        this function is used to extract the list of properties' ids (the player's properties)
    """

    items_list_str = list_str.split(",")
    items_list_str[0] = items_list_str[0][1:]
    items_list_str[len(items_list_str) - 1] = items_list_str[len(items_list_str) - 1][:len(items_list_str[len(items_list_str) - 1]) - 1]
    items_ids = []
    for i in range(len(items_list_str)):
        items_ids.append(int(items_list_str[i]))
    return items_ids

class Packet:
    def __init__(self, PlayerList = [Player]):
        PlayerList = []
        self.Player1Type1 = PlayerList[0]
        self.Player1Type2 = PlayerList[1] #a changer voir zineb #done Chris
        self.Player1Type3 = PlayerList[2] #a changer voir zineb

        self.type1 = PlayerList[0].PlayerEnum
        self.type2 = PlayerList[1].PlayerEnum
        self.type3 = PlayerList[2].PlayerEnum

        self.pos1 = PlayerList[0].pos              #on peut supprimer ces 3 et les mettre dans une seule liste c un choix a faire
        self.pos2 = PlayerList[1].pos
        self.pos3 = PlayerList[2].pos
        self.positions = [PlayerList[0].pos ,PlayerList[1].pos ,PlayerList[2].pos]

        self.attributes1 = PlayerList[0].listStat
        self.attributes2 = PlayerList[1].listStat
        self.attributes3 = PlayerList[2].listStat

        #self.propertyBag = self.extract_items_ids(player._bag._content) 


        self.enemiesHP = None #a changer une fois defini
        # un dictionnaire vide 
        #on va ajouter cet attribut a la classe player et ce dictionnaire serait rempli a chaque attaque
        #self.monsters_capacity2 = None
        #self.monsters_capacity3 = None

        self.list1 = [self.type1,self.pos1,self.attributes1]
        self.list2 = [self.type2,self.pos2,self.attributes2]
        self.list3 = [self.type3,self.pos3,self.attributes3,self.enemiesHP]
        #TODO : add bag to the last list and add equiment packet 

    def extract_items_ids(self,content):
        idItemList = []

        for item in content:
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
                packet_str += str(liste[i][j])  + "//$$//"
            packet_str += "//perso//"
        return packet_str



s="PlayerEnum.Rogue//$$//(1,2)//$$//(11,2,3,44,55,65,4,2)//$$//{1:99,2:80,3:18}//$$//[1,4,66]//$$////perso//lol//$$////perso//"
#print("".join(extract(s,"//perso//")))
#( HP, armor, strength, dex, con, intell, wis, cha )
l = read_packet(s)
print(l)
l[0][1] = read_position(l[0][1])
l[0][2] = read_attributes(l[0][2])
l[0][3] = read_monsters_dict(l[0][3])
l[0][4] = read_properties_list(l[0][4])
print(l[0][0],l[0][1],l[0][2],l[0][3],l[0][4]) 

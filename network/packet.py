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

s="(1,2)//$$//(11,2,3,44,55,65,4,2)//$$//ok essai//$$////perso//lol//$$////perso//"
#print("".join(extract(s,"//perso//")))
#( HP, armor, strength, dex, con, intell, wis, cha )
l = read_packet(s)
print(l)
l[0][0] = read_position(l[0][0])
l[0][1] = read_attributes(l[0][1])
print(l[0][0],l[0][1])

class Packet:
    def __init__(self,player):
        self.character1 = player
        self.character2 = player.crewmate[0] #a changer voir zineb
        self.character3 = player.crewmate[1] #a changer voir zineb

        self.pos1 = player.pos              #on peut supprimer ces 3 et les mettre dans une seule liste c un choix a faire
        self.pos2 = self.character2.pos
        self.pos3 = self.character3.pos
        self.positions = [player.pos,self.character2.pos,self.character3.pos]

        self.attributes1 = player.listStat
        self.attributes2 = self.character2.listStat
        self.attributes3 = self.character3.listStat

        self.properties1 = player._bag #s'assurer de zineb
        self.properties2 = self.character2._bag
        self.properties3 = self.character3._bag

        self.monsters_capacity1 = None #a definir
        self.monsters_capacity2 = None
        self.monsters_capacity3 = None

        self.list1 = [self.pos1,self.attributes1,self.properties1,self.monsters_capacity1]
        self.list2 = [self.pos2,self.attributes2,self.properties2,self.monsters_capacity2]
        self.list3 = [self.pos3,self.attributes3,self.properties3,self.monsters_capacity3]

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


    

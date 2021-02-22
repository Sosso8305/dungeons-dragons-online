import pygame
from packet import *

class OtherPlayer:
    """
    /!\ This is a test, we've not talked about it yet with zineb & christine

    For every other player, an object "OtherPlayer" will be created.
    I don't know yet how every OtherPlayer will be distinguished from each other yet.
    At the moment, i think there will be a OtherPlayer list in the GameScreen file.

    My idea is to create a method for every action involving OtherPlayer.
    These methods suggest that OtherPlayer's information have already been exctrated from packets and usable.
    (it won't be done here)

    Love u guys

    Subclasses
	----------
	None
	
	Attributes
	----------
	pos : tuple
        position of every 3 characters of the otherPlaye
    
    **may be added :
    HP : tuple
        HP of every 3 otherPlayer's characters
    equipments : ???
        the otherPlayer's equipment 

	Methods
	-------
	__init__(self, pos : tuple)
        Initialize the new OtherPlayer object (HP/equipment etc... may be added)
    updatePosition(self, pos : tuple)
        refresh the position field
    printOtherPlayer(self)
        the blitting routine of every 3 otherPlayer's characters on the gameScreen

    **may be added :
    An update method for every field we decide to add (HP, equipment)
    A "routine" method that use the other methods of the class in a specific order
    """

    def __init__(self, packet : str):
        """Initialize the new OtherPlayer object :
        * fill every field for the first time (only position atm) --> it would be interesting to add team's composition (classes)
        * add this new object to the list (which will be added to the attributes) --> not necessary for 1 otherplayer
        """
        liste_str = read_packet(packet)

        #Pour le premier perso du joueur et on reprend de meme pr les 2 autres

        self.type1 = liste_str[0][0]
        self.pos1 = read_position(liste_str[0][1])
        self.att1 = read_attributes(liste_str[0][2])
        self.monsters1 = read_monsters_dict(liste_str[0][3])
        self.items1 = read_properties_list(liste_str[0][4])

        self.type2 = liste_str[1][0]
        self.pos2 = read_position(liste_str[1][1])
        self.att2 = read_attributes(liste_str[1][2])
        self.monsters2 = read_monsters_dict(liste_str[1][3])
        self.items2 = read_properties_list(liste_str[1][4])

        self.type3 = liste_str[2][0]
        self.pos3 = read_position(liste_str[2][1])
        self.att3 = read_attributes(liste_str[2][2])
        self.monsters3 = read_monsters_dict(liste_str[2][3])
        self.items3 = read_properties_list(liste_str[2][4])

    
    def updatePosition(self, pos : tuple):
        """Will be used to refresh the position field.
        This method could be used right after receiving a position information packet.
        """
        self.pos= pos
    
    def printOtherPlayer(self):
        """To print OtherPlayer's 3 characters on the map.
        As i've not understood how it's done for the main player, i'm not able to do it yet.
        It could be used right after the init, then right after every updatePosition.
        """
        pass

s="Rogue//$$//(1,2)//$$//(11,2,3,44,55,65,4,2)//$$//{1:99,2:80,3:18}//$$//[1,4,66]//$$////perso//Sorcerer//$$//(22,3)//$$//\
(18,28,37,44,56,55,45,25)//$$//{15:9,25:60,77:18}//$$//[11,46,65]//$$//\
    //perso//Rogue//$$//(122,22)//$$//(1,22,35,45,45,33,42,20)//$$//{100:99,20:88,90:8}//$$//[100,43,63]//$$////perso//"

o = OtherPlayer(s)
print(o.type1,o.pos1,o.att1,o.monsters1,o.items1)
print(o.type2,o.pos2,o.att2,o.monsters2,o.items2)
print(o.type3,o.pos3,o.att3,o.monsters3,o.items3)
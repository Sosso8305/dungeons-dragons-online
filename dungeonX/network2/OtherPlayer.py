import pygame
from packet import *

class OtherPlayer:
    """
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
	pos1, pos2, pos3 : tuple (x,y)
        position of every 3 characters of the otherPlaye
    
    type1, type2, type3 : PlayerEnum.[Type]
        Type of every otherPlayer's characters (Mage, Rogue, Knight)
    
    att1, att2, att3 : list
        Attributes of every character (strength, wize etc)
    ennemies : dictionnary (ennemy_id,hp)
        to synchronize ennemies hp for all IRL players
        is filled with informations when the OtherPlayer deals damages
    
    items : list ?
        All items in the OtherPlayer's bag
    
    **may be added :
    hp1, hp2, hp3 : int
        hp of every 3 otherPlayer's character
	Methods
	-------
	__init__(self, packet)
        Initialize the new OtherPlayer object (HP/equipment etc... may be added)
    setPosition(self, pos : tuple)
        refresh the pos fields
    setAttributes(self, packet)
        refresh the att fields
    setEnnemies(self, packet)
        refresh the ennemies dictionnary
    printOtherPlayer(self)
        the blitting routine of every 3 otherPlayer's characters on the gameScreen
    **may be added :
    An update method for every field we decide to add (HP, equipment)
    A "routine" method that use the other methods of the class in a specific order
    A printing of otherPlayer informations when its characters are clicked
    """

    def __init__(self, packet, game):
        """Initialize the new OtherPlayer object :
        * fill every field for the first time (only position atm) --> it would be interesting to add team's composition (classes)
        * add this new object to the list (which will be added to the attributes) --> not necessary for 1 otherplayer
        """
        liste_str = read_packet(packet)

        #Pour le premier perso du joueur et on reprend de meme pr les 2 autres

        self.type1 = liste_str[0][0]
        self.pos1 = read_position(liste_str[0][1])
        self.att1 = read_attributes(liste_str[0][2])

        self.type2 = liste_str[1][0]
        self.pos2 = read_position(liste_str[1][1])
        self.att2 = read_attributes(liste_str[1][2])

        self.type3 = liste_str[2][0]
        self.pos3 = read_position(liste_str[2][1])
        self.att3 = read_attributes(liste_str[2][2])

        self.enemies = read_enemies_dict(liste_str[2][3])
        self.items = read_list(liste_str[2][4]) # a voir pour le bag et equipement

        #Initialisation des variables pour l'affichage des personnages
        """self.animationSpeed = {'idle': 120, 'run': 100} # in milliseconds
        self.game=game
        self.rect = pygame.Rect((0,0), (TILE_WIDTH, math.floor(TILE_WIDTH*24/16)))
        self.rect.midbottom = posToVect(pos) + (TILE_WIDTH/2, TILE_WIDTH)
        self.state = 'idle'
        self.direction = 0
        self._type = type"""
        #On load les images qui vont ztre utilisees 
        #et on affiche une premiere fois les personnages sur la map



    #----------Refresh otherPlayer's informations methods----------#

    def setPosition(self, packet):
        """Will be used to refresh the position field.
        This method could be used right after receiving a position information packet.
        """
        liste_str = read_packet(packet)
        self.pos1 = read_position(liste_str[0][1])
        self.pos2 = read_position(liste_str[1][1])
        self.pos3 = read_position(liste_str[2][1])

    def setAttributes(self, packet):
        liste_str = read_packet(packet)
        self.att1 = read_attributes(liste_str[0][2])
        self.att2 = read_attributes(liste_str[1][2])
        self.att3 = read_attributes(liste_str[2][2])
    
    def setEnnemies(self, packet):
        liste_str = read_packet(packet)
        self.enemies = read_enemies_dict(liste_str[2][3])
    
    #----------All blitting on the game screen methods----------#

    def printOtherPlayer(self):
        """To print OtherPlayer's 3 characters on the map.
        As i've not understood how it's done for the main player, i'm not able to do it yet.
        It could be used right after the init, then right after every updatePosition.
        """
        pass
    
    #----------Routine method----------#

    def otherPlayRoutine(self):
        """The only method that will be used in GameScreen.
        Contains all methods (reading message, extracting informations,refreshing otherPlayer's infos,blitting)
        in the right order :
        [from packet.py]
        * read_packet
        * extract 
        [from OtherPlayer.py]
        * All set methods (refreshing informations)
        * Blitting methods
        """
        pass


    #----------Tests----------#

s="PlayerEnum.Rogue//$$//(1,2)//$$//{1:11,2:2,3:3,4:44,5:55,6:65,7:4,8:2}//$$////perso//PlayerEnum.Mage//$$//(22,3)//$$//\
{1:12,2:22,3:23,4:34,5:5,6:6,7:43,8:21}//$$////perso//PlayerEnum.Rogue//$$//(122,22)//$$//{1:22,2:2,3:3,4:14,5:25,6:75,7:5,8:3}//$$//{100:99,20:88,90:8}//$$//[100,43,63]//$$////perso//"

o = OtherPlayer(s)
print(o.type1,o.pos1,o.att1)
print(o.type2,o.pos2,o.att2)
print(o.type3,o.pos3,o.att3,o.enemies,o.items)
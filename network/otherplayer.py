import pygame

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

    def __init__(self, pos : tuple):
        """Initialize the new OtherPlayer object :
        * fill every field for the first time (only position atm) --> it would be interesting to add team's composition (classes)
        * add this new object to the list (which will be added to the attributes) --> not necessary for 1 otherplayer
        """
        self.pos= pos
    
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
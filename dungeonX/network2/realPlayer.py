from dungeonX.characters import Bag
from dungeonX.constants import OTHERPLAYERNAME,DEFAULT_ACTION_POINT
from dungeonX.characters.character import Character
from dungeonX.network.message import read_position

class RealPlayer():

    def __init__(self,oplayers,name = OTHERPLAYERNAME):
       
        self.name = name
        self.persos = oplayers
        self.bag = Bag(500)
        for player in oplayers:
            player.parent = self
            player.name = name
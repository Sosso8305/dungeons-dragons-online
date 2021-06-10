#from dungeonX.characters import Bag
from dungeonX.constants import OTHERPLAYERNAME,DEFAULT_ACTION_POINT
from dungeonX.characters.character import Character
from dungeonX.network.message import read_position
from ..constants import ItemAttributes, ItemList

class RealPlayer():

    def __init__(self,oplayers,name = OTHERPLAYERNAME):
       
        self.name = name
        self.persos = oplayers
        self.itemsList = []
        for player in oplayers:
            player.parent = self
            player.name = name
    
    def getCurrentWeight(self):
        currentWeight = sum([item.getWeight() for item in self.itemsList])
        return currentWeight

    def getBalance(self):
        return sum([item.getValue() for item in self.itemsList if item.getItemType() == ItemList.Coin])